"""
Profile Routes
===============
Handles user profile CRUD operations.

Endpoints:
    GET  /api/profile       - Get user profile
    PUT  /api/profile       - Update user profile
    GET  /api/profile/targets - Get computed BMR/TDEE/macro targets

Cloud Computing Concepts Demonstrated:
- Cloud Database CRUD: Create, Read, Update operations
- User Data Isolation: Each user accesses only their own profile
- Server-side Computation: BMR/TDEE calculated on backend (prevents tampering)
"""

import json
from flask import Blueprint, request, jsonify
from models.database import get_db
from utils.auth_helpers import token_required
from utils.validators import validate_profile, sanitize_string, parse_json_field
from services.nutrition_service import compute_targets

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('', methods=['GET'])
@token_required
def get_profile(user_id):
    """
    Get the authenticated user's profile.
    
    Returns:
        200: User profile data
        404: Profile not found
    """
    db = get_db()
    user = db.execute(
        '''SELECT user_id, name, email, age, height_cm, weight_kg, sex,
                  activity_level, dietary_preference, goal, allergies,
                  cuisines, budget_per_day, timeline_weeks, profile_completed,
                  created_at, updated_at
           FROM users WHERE user_id = ?''',
        (user_id,)
    ).fetchone()
    db.close()

    if not user:
        return jsonify({'error': 'Profile not found'}), 404

    profile = dict(user)
    profile['allergies'] = parse_json_field(profile.get('allergies', '[]'))
    profile['cuisines'] = parse_json_field(profile.get('cuisines', '[]'))
    profile['profile_completed'] = bool(profile.get('profile_completed', 0))

    return jsonify({'profile': profile}), 200


@profile_bp.route('', methods=['PUT'])
@token_required
def update_profile(user_id):
    """
    Update the authenticated user's profile.
    
    Request Body (all fields optional):
        {
            "name": "Demo User",
            "age": 25,
            "height_cm": 170,
            "weight_kg": 68,
            "sex": "male",
            "activity_level": "moderate",
            "dietary_preference": "vegetarian",
            "goal": "maintain",
            "allergies": ["nuts", "lactose"],
            "cuisines": ["indian", "mediterranean"],
            "budget_per_day": 300,
            "timeline_weeks": 8
        }
    
    Returns:
        200: Profile updated successfully
        400: Validation error
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    # Validate profile data
    is_valid, error_msg = validate_profile(data)
    if not is_valid:
        return jsonify({'error': error_msg}), 400

    # Build update query dynamically
    allowed_fields = [
        'name', 'age', 'height_cm', 'weight_kg', 'sex',
        'activity_level', 'dietary_preference', 'goal',
        'allergies', 'cuisines', 'budget_per_day', 'timeline_weeks'
    ]

    updates = []
    values = []
    for field in allowed_fields:
        if field in data:
            if field in ('allergies', 'cuisines'):
                updates.append(f'{field} = ?')
                values.append(json.dumps(data[field]) if isinstance(data[field], list) else data[field])
            elif field == 'name':
                updates.append(f'{field} = ?')
                values.append(sanitize_string(data[field]))
            else:
                updates.append(f'{field} = ?')
                values.append(data[field])

    if not updates:
        return jsonify({'error': 'No valid fields to update'}), 400

    # Mark profile as completed if key fields are present
    updates.append('profile_completed = ?')
    db = get_db()
    user = db.execute(
        'SELECT age, height_cm, weight_kg FROM users WHERE user_id = ?',
        (user_id,)
    ).fetchone()

    # Check if profile is complete (existing + new data)
    merged = dict(user) if user else {}
    merged.update({k: v for k, v in data.items() if v is not None})
    profile_complete = all(merged.get(f) for f in ['age', 'height_cm', 'weight_kg'])
    values.append(1 if profile_complete else 0)

    updates.append("updated_at = datetime('now')")
    values.append(user_id)

    query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
    db.execute(query, values)
    db.commit()
    db.close()

    return jsonify({
        'message': 'Profile updated successfully',
        'profile_completed': profile_complete
    }), 200


@profile_bp.route('/targets', methods=['GET'])
@token_required
def get_nutrition_targets(user_id):
    """
    Compute and return BMR, TDEE, and macro targets based on user profile.
    Server-side computation prevents client-side tampering.
    
    Returns:
        200: Computed nutrition targets
        400: Incomplete profile
    """
    db = get_db()
    user = db.execute(
        '''SELECT age, height_cm, weight_kg, sex, activity_level, goal
           FROM users WHERE user_id = ?''',
        (user_id,)
    ).fetchone()
    db.close()

    if not user:
        return jsonify({'error': 'Profile not found'}), 404

    if not all([user['age'], user['height_cm'], user['weight_kg']]):
        return jsonify({'error': 'Please complete your profile first (age, height, weight required)'}), 400

    targets = compute_targets(
        sex=user['sex'] or 'not_specified',
        weight_kg=float(user['weight_kg']),
        height_cm=float(user['height_cm']),
        age=int(user['age']),
        activity_level=user['activity_level'] or 'moderate',
        goal=user['goal'] or 'maintain'
    )

    return jsonify({'targets': targets}), 200
