"""
Input Validators
=================
Validation utilities for user inputs.
Ensures data integrity before processing or storage.
"""

import re
import json


def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    if not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple:
    """
    Validate password strength.
    Returns (is_valid, error_message).
    """
    if not isinstance(password, str):
        return False, "Password must be a string"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, ""


def validate_profile(data: dict) -> tuple:
    """
    Validate user profile data.
    Returns (is_valid, error_message).
    """
    if not isinstance(data, dict):
        return False, "Profile payload must be an object"

    # Age validation
    age = data.get('age')
    if age is not None:
        try:
            age = int(age)
            if age < 10 or age > 120:
                return False, "Age must be between 10 and 120"
        except (ValueError, TypeError):
            return False, "Age must be a valid number"

    # Height validation
    height = data.get('height_cm')
    if height is not None:
        try:
            height = float(height)
            if height < 50 or height > 300:
                return False, "Height must be between 50 and 300 cm"
        except (ValueError, TypeError):
            return False, "Height must be a valid number"

    # Weight validation
    weight = data.get('weight_kg')
    if weight is not None:
        try:
            weight = float(weight)
            if weight < 20 or weight > 500:
                return False, "Weight must be between 20 and 500 kg"
        except (ValueError, TypeError):
            return False, "Weight must be a valid number"

    # Activity level validation
    valid_activities = ['sedentary', 'light', 'moderate', 'active', 'very_active']
    activity = data.get('activity_level')
    if activity is not None:
        activity = str(activity).strip().lower()
        if activity not in valid_activities:
            return False, f"Activity level must be one of: {', '.join(valid_activities)}"

    # Dietary preference validation
    valid_diets = ['vegetarian', 'vegan', 'non_vegetarian', 'eggetarian']
    diet = data.get('dietary_preference')
    if diet is not None:
        diet = str(diet).strip().lower()
        if diet not in valid_diets:
            return False, f"Dietary preference must be one of: {', '.join(valid_diets)}"

    # Goal validation
    valid_goals = ['lose_weight', 'gain_weight', 'maintain', 'muscle_gain', 'general_fitness']
    goal = data.get('goal')
    if goal is not None:
        goal = str(goal).strip().lower()
        if goal not in valid_goals:
            return False, f"Goal must be one of: {', '.join(valid_goals)}"

    # Sex validation
    valid_sex = ['male', 'female', 'not_specified']
    sex = data.get('sex')
    if sex is not None:
        sex = str(sex).strip().lower()
        if sex not in valid_sex:
            return False, f"Sex must be one of: {', '.join(valid_sex)}"

    # Lists like allergies and cuisines must be arrays of strings when supplied.
    for key in ('allergies', 'cuisines'):
        if key in data and data[key] is not None:
            value = data[key]
            if isinstance(value, str):
                try:
                    parsed = json.loads(value)
                    if not isinstance(parsed, list):
                        return False, f"{key} must be a list of strings"
                    if not all(isinstance(item, str) for item in parsed):
                        return False, f"{key} must be a list of strings"
                except json.JSONDecodeError:
                    return False, f"{key} must be a list of strings"
            elif not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                return False, f"{key} must be a list of strings"

    return True, ""


def sanitize_string(value: str) -> str:
    """Remove potentially dangerous characters from input strings."""
    if not isinstance(value, str):
        return str(value)
    # Remove HTML tags and trim whitespace
    clean = re.sub(r'<[^>]*>', '', value)
    return clean.strip()


def parse_json_field(value) -> list:
    """Parse a JSON string field or return as-is if already a list."""
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass
    return []
