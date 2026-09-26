"""
Diet Plan Routes
=================
Handles diet plan generation, retrieval, and management.

Endpoints:
    POST   /api/plans/generate    - Generate a new AI diet plan
    GET    /api/plans             - Get all plans for the user
    GET    /api/plans/<plan_id>   - Get a specific plan
    DELETE /api/plans/<plan_id>   - Delete a plan

Cloud Computing Concepts Demonstrated:
- AI Integration: AI-powered plan generation with fallback
- Cloud Database: Storing and retrieving structured plan data
- REST API: Full CRUD operations
- User Data Isolation: Users can only access their own plans
"""

import json
from flask import Blueprint, request, jsonify
from models.database import get_db
from utils.auth_helpers import token_required, generate_plan_id
from services.nutrition_service import compute_targets

# Import the AI diet engine
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ai_engine'))
from diet_engine import DietEngine

plan_bp = Blueprint('plans', __name__)
diet_engine = DietEngine()


@plan_bp.route('/generate', methods=['POST'])
@token_required
def generate_plan(user_id):
    """
    Generate a new personalized diet plan using the AI engine.
    
    The plan is generated based on the user's profile (dietary preference,
    activity level, goal, allergies) and computed nutrition targets.
    
    Request Body (optional overrides):
        {
            "diet_type": "vegetarian",   
            "goal": "lose_weight",       
            "plan_name": "My Weekly Plan"
        }
    
    Returns:
        201: Generated plan with meals and nutrition summary
        400: Incomplete profile
    
    DISCLAIMER: Generated plans are for educational/general wellness 
    demonstration only and NOT medical or clinical nutrition advice.
    """
    data = request.get_json() or {}

    # Fetch user profile
    db = get_db()
    user = db.execute(
        '''SELECT name, age, height_cm, weight_kg, sex, activity_level,
                  dietary_preference, goal, allergies, cuisines
           FROM users WHERE user_id = ?''',
        (user_id,)
    ).fetchone()

    if not user:
        db.close()
        return jsonify({'error': 'User not found'}), 404

    if not all([user['age'], user['height_cm'], user['weight_kg']]):
        db.close()
        return jsonify({'error': 'Please complete your profile first'}), 400

    # Determine plan parameters (allow request overrides)
    diet_type = data.get('diet_type', user['dietary_preference'] or 'vegetarian')
    goal = data.get('goal', user['goal'] or 'maintain')
    plan_name = data.get('plan_name', 'My Diet Plan')

    # Compute nutrition targets
    targets = compute_targets(
        sex=user['sex'] or 'not_specified',
        weight_kg=float(user['weight_kg']),
        height_cm=float(user['height_cm']),
        age=int(user['age']),
        activity_level=user['activity_level'] or 'moderate',
        goal=goal
    )

    # Parse allergies
    allergies = []
    try:
        allergies = json.loads(user['allergies']) if user['allergies'] else []
    except (json.JSONDecodeError, TypeError):
        allergies = []

    # Generate plan using AI engine
    plan = diet_engine.generate_plan(
        daily_calories=targets['daily_calories'],
        macros=targets['macros'],
        diet_type=diet_type,
        goal=goal,
        allergies=allergies
    )

    # Save plan to database
    plan_id = generate_plan_id()
    db.execute(
        '''INSERT INTO diet_plans 
           (plan_id, user_id, plan_name, breakfast, lunch, snack, dinner,
            total_calories, protein_g, carbs_g, fat_g, nutrition_summary,
            hydration_reminder, diet_type, goal_type)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            plan_id, user_id, plan_name,
            json.dumps(plan['breakfast']),
            json.dumps(plan['lunch']),
            json.dumps(plan['snack']),
            json.dumps(plan['dinner']),
            plan['total_calories'],
            plan['macros']['protein_g'],
            plan['macros']['carbs_g'],
            plan['macros']['fat_g'],
            plan['nutrition_summary'],
            plan['hydration_reminder'],
            diet_type, goal
        )
    )
    db.commit()
    db.close()

    return jsonify({
        'message': 'Diet plan generated successfully',
        'disclaimer': 'This plan is for educational/general wellness demonstration only. It is NOT medical or clinical nutrition advice.',
        'plan': {
            'plan_id': plan_id,
            'plan_name': plan_name,
            'breakfast': plan['breakfast'],
            'lunch': plan['lunch'],
            'snack': plan['snack'],
            'dinner': plan['dinner'],
            'total_calories': plan['total_calories'],
            'macros': plan['macros'],
            'nutrition_summary': plan['nutrition_summary'],
            'hydration_reminder': plan['hydration_reminder'],
            'targets': targets,
            'diet_type': diet_type,
            'goal': goal
        }
    }), 201


@plan_bp.route('', methods=['GET'])
@token_required
def get_plans(user_id):
    """
    Get all diet plans for the authenticated user.
    Returns plans sorted by creation date (newest first).
    """
    db = get_db()
    plans = db.execute(
        '''SELECT plan_id, plan_name, total_calories, protein_g, carbs_g,
                  fat_g, diet_type, goal_type, created_at
           FROM diet_plans WHERE user_id = ? ORDER BY created_at DESC''',
        (user_id,)
    ).fetchall()
    db.close()

    plan_list = []
    for p in plans:
        plan_list.append({
            'plan_id': p['plan_id'],
            'plan_name': p['plan_name'],
            'total_calories': p['total_calories'],
            'protein_g': p['protein_g'],
            'carbs_g': p['carbs_g'],
            'fat_g': p['fat_g'],
            'diet_type': p['diet_type'],
            'goal_type': p['goal_type'],
            'created_at': p['created_at']
        })

    return jsonify({'plans': plan_list, 'count': len(plan_list)}), 200


@plan_bp.route('/<plan_id>', methods=['GET'])
@token_required
def get_plan(user_id, plan_id):
    """
    Get a specific diet plan by ID.
    Only returns the plan if it belongs to the authenticated user (data isolation).
    """
    db = get_db()
    plan = db.execute(
        '''SELECT * FROM diet_plans WHERE plan_id = ? AND user_id = ?''',
        (plan_id, user_id)
    ).fetchone()
    db.close()

    if not plan:
        return jsonify({'error': 'Plan not found'}), 404

    return jsonify({
        'plan': {
            'plan_id': plan['plan_id'],
            'plan_name': plan['plan_name'],
            'breakfast': json.loads(plan['breakfast']),
            'lunch': json.loads(plan['lunch']),
            'snack': json.loads(plan['snack']),
            'dinner': json.loads(plan['dinner']),
            'total_calories': plan['total_calories'],
            'macros': {
                'protein_g': plan['protein_g'],
                'carbs_g': plan['carbs_g'],
                'fat_g': plan['fat_g']
            },
            'nutrition_summary': plan['nutrition_summary'],
            'hydration_reminder': plan['hydration_reminder'],
            'diet_type': plan['diet_type'],
            'goal_type': plan['goal_type'],
            'created_at': plan['created_at']
        },
        'disclaimer': 'This plan is for educational/general wellness demonstration only.'
    }), 200


@plan_bp.route('/<plan_id>', methods=['DELETE'])
@token_required
def delete_plan(user_id, plan_id):
    """
    Delete a diet plan.
    Only the plan owner can delete it (authorization check).
    """
    db = get_db()

    # Verify ownership
    plan = db.execute(
        'SELECT plan_id FROM diet_plans WHERE plan_id = ? AND user_id = ?',
        (plan_id, user_id)
    ).fetchone()

    if not plan:
        db.close()
        return jsonify({'error': 'Plan not found'}), 404

    db.execute('DELETE FROM diet_plans WHERE plan_id = ?', (plan_id,))
    db.commit()
    db.close()

    return jsonify({'message': 'Plan deleted successfully'}), 200
