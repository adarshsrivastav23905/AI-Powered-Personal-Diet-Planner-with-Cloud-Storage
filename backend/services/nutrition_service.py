"""
Nutrition Service
==================
Server-side BMR/TDEE computation and macro target calculation.

Uses the Mifflin-St Jeor equation for BMR estimation.

Cloud Computing Concept Demonstrated:
- Server-side Processing: Calculations done on backend to prevent tampering
- Microservice Architecture: Isolated service for nutrition logic
"""

import math


# Physical Activity Level multipliers
PAL_MULTIPLIERS = {
    'sedentary': 1.2,       # Little or no exercise
    'light': 1.375,         # Light exercise 1-3 days/week
    'moderate': 1.55,       # Moderate exercise 3-5 days/week
    'active': 1.725,        # Hard exercise 6-7 days/week
    'very_active': 1.9      # Very hard exercise & physical job
}

# Goal calorie adjustments
GOAL_ADJUSTMENTS = {
    'lose_weight': -0.15,     # 15% caloric deficit
    'gain_weight': 0.15,      # 15% caloric surplus
    'maintain': 0.0,          # Maintenance calories
    'muscle_gain': 0.10,      # 10% surplus for lean gains
    'general_fitness': 0.0    # Maintenance with balanced macros
}

# Macro splits (protein%, carbs%, fat%) by goal
MACRO_SPLITS = {
    'lose_weight': (0.35, 0.35, 0.30),      # Higher protein for satiety
    'gain_weight': (0.25, 0.50, 0.25),       # Higher carbs for energy
    'maintain': (0.30, 0.40, 0.30),          # Balanced
    'muscle_gain': (0.35, 0.40, 0.25),       # High protein
    'general_fitness': (0.30, 0.40, 0.30)    # Balanced
}


def compute_bmr(sex: str, weight_kg: float, height_cm: float, age: int) -> float:
    """
    Compute Basal Metabolic Rate using Mifflin-St Jeor equation.
    
    Formula:
        Male:   BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
        Female: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161
    
    Args:
        sex: 'male', 'female', or 'not_specified'
        weight_kg: Body weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
    
    Returns:
        BMR in kcal/day
    """
    base = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    if sex == 'male':
        return base + 5
    elif sex == 'female':
        return base - 161
    else:
        # Average of male and female for unspecified
        return base - 78


def compute_tdee(bmr: float, activity_level: str) -> float:
    """
    Compute Total Daily Energy Expenditure.
    TDEE = BMR × Physical Activity Level multiplier
    """
    multiplier = PAL_MULTIPLIERS.get(activity_level, 1.2)
    return bmr * multiplier


def compute_targets(sex: str, weight_kg: float, height_cm: float,
                    age: int, activity_level: str, goal: str) -> dict:
    """
    Compute complete nutrition targets for a user.
    
    Returns:
        {
            'bmr': int,
            'tdee': int,
            'daily_calories': int,
            'macros': {
                'protein_g': int,
                'carbs_g': int,
                'fat_g': int
            },
            'goal_adjustment': str,
            'water_liters': float
        }
    """
    bmr = compute_bmr(sex, weight_kg, height_cm, age)
    tdee = compute_tdee(bmr, activity_level)

    # Apply goal adjustment
    adjustment = GOAL_ADJUSTMENTS.get(goal, 0.0)
    daily_calories = math.floor(tdee * (1 + adjustment))

    # Calculate macros based on goal
    p_pct, c_pct, f_pct = MACRO_SPLITS.get(goal, (0.30, 0.40, 0.30))

    macros = {
        'protein_g': round((p_pct * daily_calories) / 4),   # 4 kcal per gram protein
        'carbs_g': round((c_pct * daily_calories) / 4),     # 4 kcal per gram carbs
        'fat_g': round((f_pct * daily_calories) / 9)        # 9 kcal per gram fat
    }

    # Water recommendation: ~30-35 ml per kg body weight
    water_liters = round(weight_kg * 0.033, 1)

    return {
        'bmr': round(bmr),
        'tdee': round(tdee),
        'daily_calories': daily_calories,
        'macros': macros,
        'goal_adjustment': f"{'+' if adjustment > 0 else ''}{int(adjustment*100)}%",
        'water_liters': water_liters
    }
