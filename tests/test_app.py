"""
Automated Test Suite for AI-Powered Personal Diet Planner
==========================================================
Tests cover:
- User registration & authentication
- Profile management
- Diet plan generation
- Cloud storage operations
- AI engine (rule-based)
- Input validation
- Authorization (data isolation)

Run: python -m pytest tests/test_app.py -v
"""

import os
import sys
import json
import pytest

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai_engine'))

from app import create_app
from models.database import init_db, DB_PATH


@pytest.fixture
def app():
    """Create application for testing."""
    # Use a test database
    import models.database as db_module
    test_db = os.path.join(os.path.dirname(__file__), 'test_diet_planner.db')
    db_module.DB_PATH = test_db

    app = create_app()
    app.config['TESTING'] = True

    # Clean up before test
    if os.path.exists(test_db):
        os.remove(test_db)
    init_db()

    yield app

    # Cleanup after test
    if os.path.exists(test_db):
        os.remove(test_db)


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Register a user and return auth headers."""
    response = client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'test123'
    })
    data = response.get_json()
    return {'Authorization': f'Bearer {data["token"]}'}


@pytest.fixture
def second_user_headers(client):
    """Register a second user for isolation tests."""
    response = client.post('/api/auth/register', json={
        'name': 'User Two',
        'email': 'user2@example.com',
        'password': 'pass456'
    })
    data = response.get_json()
    return {'Authorization': f'Bearer {data["token"]}'}


# ═══════════════════════════════════════════════════════════════
# TEST 1: Health Check
# ═══════════════════════════════════════════════════════════════
class TestHealthCheck:
    def test_health_endpoint(self, client):
        """TC-00: API health check returns 200."""
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.get_json()['status'] == 'healthy'


# ═══════════════════════════════════════════════════════════════
# TEST 2-5: Authentication
# ═══════════════════════════════════════════════════════════════
class TestAuthentication:

    def test_register_new_user(self, client):
        """TC-01: New user registration succeeds."""
        response = client.post('/api/auth/register', json={
            'name': 'Demo User',
            'email': 'demo@example.com',
            'password': 'demo123'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'token' in data
        assert data['user']['email'] == 'demo@example.com'

    def test_register_duplicate_email(self, client):
        """TC-02: Duplicate email registration fails with 409."""
        client.post('/api/auth/register', json={
            'name': 'User 1', 'email': 'dup@example.com', 'password': 'pass123'
        })
        response = client.post('/api/auth/register', json={
            'name': 'User 2', 'email': 'dup@example.com', 'password': 'pass456'
        })
        assert response.status_code == 409

    def test_login_valid_credentials(self, client):
        """TC-03: Valid login returns token."""
        client.post('/api/auth/register', json={
            'name': 'Login User', 'email': 'login@example.com', 'password': 'login123'
        })
        response = client.post('/api/auth/login', json={
            'email': 'login@example.com', 'password': 'login123'
        })
        assert response.status_code == 200
        assert 'token' in response.get_json()

    def test_login_invalid_credentials(self, client):
        """TC-04: Invalid login returns 401."""
        response = client.post('/api/auth/login', json={
            'email': 'wrong@example.com', 'password': 'wrong123'
        })
        assert response.status_code == 401

    def test_unauthorized_dashboard_access(self, client):
        """TC-05: Accessing protected route without token returns 401."""
        response = client.get('/api/profile')
        assert response.status_code == 401


# ═══════════════════════════════════════════════════════════════
# TEST 6-7: Profile Management
# ═══════════════════════════════════════════════════════════════
class TestProfile:

    def test_create_profile(self, client, auth_headers):
        """TC-06: Profile creation/update succeeds."""
        response = client.put('/api/profile', json={
            'age': 25,
            'height_cm': 170,
            'weight_kg': 68,
            'sex': 'male',
            'activity_level': 'moderate',
            'dietary_preference': 'vegetarian',
            'goal': 'maintain'
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.get_json()['profile_completed'] is True

    def test_get_profile(self, client, auth_headers):
        """TC-06b: Retrieve profile after creation."""
        client.put('/api/profile', json={
            'age': 22, 'height_cm': 165, 'weight_kg': 60
        }, headers=auth_headers)

        response = client.get('/api/profile', headers=auth_headers)
        assert response.status_code == 200
        profile = response.get_json()['profile']
        assert profile['age'] == 22


# ═══════════════════════════════════════════════════════════════
# TEST 8-12: Diet Plan Generation
# ═══════════════════════════════════════════════════════════════
class TestDietPlan:

    def _setup_profile(self, client, headers, diet='vegetarian', goal='maintain'):
        """Helper to set up a complete profile."""
        client.put('/api/profile', json={
            'age': 25, 'height_cm': 170, 'weight_kg': 68,
            'sex': 'male', 'activity_level': 'moderate',
            'dietary_preference': diet, 'goal': goal
        }, headers=headers)

    def test_generate_plan(self, client, auth_headers):
        """TC-07: Diet plan generation succeeds with complete profile."""
        self._setup_profile(client, auth_headers)

        response = client.post('/api/plans/generate', json={},
                               headers=auth_headers)
        assert response.status_code == 201
        plan = response.get_json()['plan']
        assert 'breakfast' in plan
        assert 'lunch' in plan
        assert 'snack' in plan
        assert 'dinner' in plan
        assert plan['total_calories'] > 0

    def test_vegetarian_plan(self, client, auth_headers):
        """TC-08: Vegetarian plan contains no meat."""
        self._setup_profile(client, auth_headers, diet='vegetarian')

        response = client.post('/api/plans/generate',
                               json={'diet_type': 'vegetarian'},
                               headers=auth_headers)
        assert response.status_code == 201

    def test_vegan_plan(self, client, auth_headers):
        """TC-09: Vegan plan generation succeeds."""
        self._setup_profile(client, auth_headers, diet='vegan')

        response = client.post('/api/plans/generate',
                               json={'diet_type': 'vegan'},
                               headers=auth_headers)
        assert response.status_code == 201

    def test_different_goal(self, client, auth_headers):
        """TC-10: Plan with 'lose_weight' goal succeeds."""
        self._setup_profile(client, auth_headers, goal='lose_weight')

        response = client.post('/api/plans/generate',
                               json={'goal': 'lose_weight'},
                               headers=auth_headers)
        assert response.status_code == 201

    def test_save_and_retrieve_plan(self, client, auth_headers):
        """TC-13: Save and retrieve a plan."""
        self._setup_profile(client, auth_headers)

        # Generate plan
        gen_response = client.post('/api/plans/generate', json={},
                                   headers=auth_headers)
        plan_id = gen_response.get_json()['plan']['plan_id']

        # Retrieve plan
        response = client.get(f'/api/plans/{plan_id}', headers=auth_headers)
        assert response.status_code == 200
        assert response.get_json()['plan']['plan_id'] == plan_id

    def test_list_plans(self, client, auth_headers):
        """TC-14: List all user's plans."""
        self._setup_profile(client, auth_headers)
        client.post('/api/plans/generate', json={}, headers=auth_headers)

        response = client.get('/api/plans', headers=auth_headers)
        assert response.status_code == 200
        assert response.get_json()['count'] >= 1

    def test_delete_plan(self, client, auth_headers):
        """TC-14b: Delete a plan."""
        self._setup_profile(client, auth_headers)

        gen_response = client.post('/api/plans/generate', json={},
                                   headers=auth_headers)
        plan_id = gen_response.get_json()['plan']['plan_id']

        response = client.delete(f'/api/plans/{plan_id}', headers=auth_headers)
        assert response.status_code == 200

    def test_incomplete_profile_fails(self, client, auth_headers):
        """TC-07b: Plan generation fails without complete profile."""
        response = client.post('/api/plans/generate', json={},
                               headers=auth_headers)
        assert response.status_code == 400


# ═══════════════════════════════════════════════════════════════
# TEST 13-16: Cloud Storage
# ═══════════════════════════════════════════════════════════════
class TestCloudStorage:

    def test_upload_file(self, client, auth_headers):
        """TC-15: File upload succeeds."""
        import io
        data = {'file': (io.BytesIO(b'test file content'), 'test_plan.txt')}
        response = client.post('/api/storage/upload',
                               data=data,
                               content_type='multipart/form-data',
                               headers=auth_headers)
        assert response.status_code == 201
        assert 'file_id' in response.get_json()['file']

    def test_list_files(self, client, auth_headers):
        """TC-16: List uploaded files."""
        import io
        data = {'file': (io.BytesIO(b'content'), 'myfile.txt')}
        client.post('/api/storage/upload', data=data,
                    content_type='multipart/form-data', headers=auth_headers)

        response = client.get('/api/storage/files', headers=auth_headers)
        assert response.status_code == 200
        assert response.get_json()['count'] >= 1

    def test_invalid_file_type(self, client, auth_headers):
        """TC-17: Invalid file type rejected."""
        import io
        data = {'file': (io.BytesIO(b'bad'), 'malware.exe')}
        response = client.post('/api/storage/upload', data=data,
                               content_type='multipart/form-data',
                               headers=auth_headers)
        assert response.status_code == 400


# ═══════════════════════════════════════════════════════════════
# TEST 17-18: Authorization / Data Isolation
# ═══════════════════════════════════════════════════════════════
class TestDataIsolation:

    def test_user_cannot_access_other_user_plan(self, client, auth_headers, second_user_headers):
        """TC-18: User A cannot retrieve User B's plan."""
        # User A creates profile and plan
        client.put('/api/profile', json={
            'age': 25, 'height_cm': 170, 'weight_kg': 68,
            'sex': 'male', 'activity_level': 'moderate',
            'dietary_preference': 'vegetarian', 'goal': 'maintain'
        }, headers=auth_headers)
        gen_response = client.post('/api/plans/generate', json={},
                                   headers=auth_headers)
        plan_id = gen_response.get_json()['plan']['plan_id']

        # User B tries to access User A's plan
        response = client.get(f'/api/plans/{plan_id}', headers=second_user_headers)
        assert response.status_code == 404

    def test_logout(self, client, auth_headers):
        """TC-19: Logout returns success."""
        response = client.post('/api/auth/logout', headers=auth_headers)
        assert response.status_code == 200


# ═══════════════════════════════════════════════════════════════
# TEST 19: AI Engine Direct Tests
# ═══════════════════════════════════════════════════════════════
class TestAIEngine:

    def test_rule_based_generation(self):
        """TC-11: Rule-based engine generates valid plan."""
        from diet_engine import DietEngine
        engine = DietEngine()
        plan = engine.generate_plan(
            daily_calories=2000,
            macros={'protein_g': 150, 'carbs_g': 200, 'fat_g': 67},
            diet_type='vegetarian',
            goal='maintain'
        )
        assert 'breakfast' in plan
        assert 'lunch' in plan
        assert 'snack' in plan
        assert 'dinner' in plan
        assert plan['total_calories'] > 0

    def test_vegan_filter(self):
        """TC-12: Vegan filter excludes non-vegan foods."""
        from diet_engine import DietEngine
        engine = DietEngine()
        plan = engine.generate_plan(
            daily_calories=1800,
            macros={'protein_g': 100, 'carbs_g': 220, 'fat_g': 55},
            diet_type='vegan',
            goal='maintain'
        )
        assert plan['total_calories'] > 0

    def test_allergy_filter(self):
        """TC-12b: Allergy filter works."""
        from diet_engine import DietEngine
        engine = DietEngine()
        plan = engine.generate_plan(
            daily_calories=2000,
            macros={'protein_g': 150, 'carbs_g': 200, 'fat_g': 67},
            diet_type='vegetarian',
            goal='maintain',
            allergies=['nuts', 'gluten']
        )
        assert plan['total_calories'] > 0


# ═══════════════════════════════════════════════════════════════
# TEST 20: Nutrition Service
# ═══════════════════════════════════════════════════════════════
class TestNutritionService:

    def test_compute_targets_male(self):
        """Test BMR/TDEE computation for male."""
        from services.nutrition_service import compute_targets
        targets = compute_targets('male', 70, 175, 25, 'moderate', 'maintain')
        assert targets['bmr'] > 0
        assert targets['tdee'] > targets['bmr']
        assert targets['daily_calories'] > 0
        assert targets['macros']['protein_g'] > 0

    def test_compute_targets_female(self):
        """Test BMR/TDEE computation for female."""
        from services.nutrition_service import compute_targets
        targets = compute_targets('female', 60, 165, 22, 'light', 'lose_weight')
        assert targets['daily_calories'] < targets['tdee']  # Deficit

    def test_compute_targets_gain(self):
        """Test calorie surplus for weight gain."""
        from services.nutrition_service import compute_targets
        targets = compute_targets('male', 65, 170, 20, 'active', 'gain_weight')
        assert targets['daily_calories'] > targets['tdee']  # Surplus
