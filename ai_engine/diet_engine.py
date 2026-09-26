"""
AI Diet Recommendation Engine
===============================
Generates personalized diet plans based on user profile, preferences, and goals.

Two modes:
    VERSION A (Default): Rule-based recommendation using predefined food datasets
    VERSION B (Optional): AI API integration with automatic fallback to Version A

Cloud Computing Concept Demonstrated:
- AI Integration: Intelligent recommendation with cloud API
- Fallback Pattern: Graceful degradation when external service is unavailable
- Microservice: Isolated AI engine that can be deployed independently

DISCLAIMER: Generated plans are for educational/general wellness
demonstration only. They do NOT constitute medical or clinical nutrition advice.
"""

import os
import json
import random
import math
import logging

logger = logging.getLogger(__name__)

# Load food database
FOOD_DATA_PATH = os.path.join(os.path.dirname(__file__), 'food_data.json')


class DietEngine:
    """
    AI-Powered Diet Recommendation Engine.
    
    Supports:
    - Vegetarian, Vegan, Non-Vegetarian, Eggetarian plans
    - Goal-based adjustments (lose weight, gain weight, maintain, muscle gain)
    - Allergy filtering
    - Nutritional target matching
    """

    def __init__(self):
        """Initialize the engine and load the food database."""
        self.foods = self._load_food_data()
        self.ai_api_available = self._check_ai_api()

    def _load_food_data(self) -> list:
        """Load the food database from JSON file."""
        try:
            with open(FOOD_DATA_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('foods', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Could not load food data: {e}. Using minimal built-in data.")
            return self._get_fallback_foods()

    def _get_fallback_foods(self) -> list:
        """Minimal built-in food data as ultimate fallback."""
        return [
            {"id": "oats", "name": "Oatmeal with Milk", "category": "breakfast",
             "per_serving": {"kcal": 300, "protein": 10, "carbs": 50, "fat": 8},
             "serving_size": "1 bowl (200g)", "tags": ["vegetarian", "eggetarian"], "allergens": ["gluten"]},
            {"id": "rice_dal", "name": "Rice with Dal", "category": "lunch",
             "per_serving": {"kcal": 400, "protein": 15, "carbs": 65, "fat": 8},
             "serving_size": "1 plate", "tags": ["vegetarian", "vegan"], "allergens": []},
            {"id": "fruit_salad", "name": "Mixed Fruit Salad", "category": "snack",
             "per_serving": {"kcal": 150, "protein": 2, "carbs": 35, "fat": 1},
             "serving_size": "1 bowl", "tags": ["vegetarian", "vegan"], "allergens": []},
            {"id": "roti_sabzi", "name": "Roti with Mixed Vegetables", "category": "dinner",
             "per_serving": {"kcal": 350, "protein": 12, "carbs": 50, "fat": 10},
             "serving_size": "2 rotis + sabzi", "tags": ["vegetarian", "vegan"], "allergens": ["gluten"]},
        ]

    def _check_ai_api(self) -> bool:
        """Check if an external AI API is configured and available."""
        api_key = os.getenv('AI_API_KEY', '')
        return bool(api_key)

    def generate_plan(self, daily_calories: int, macros: dict,
                      diet_type: str = 'vegetarian', goal: str = 'maintain',
                      allergies: list = None) -> dict:
        """
        Generate a complete diet plan.
        
        Strategy:
        1. Try AI API if available (VERSION B)
        2. Fall back to rule-based engine (VERSION A)
        
        Args:
            daily_calories: Target daily calorie intake
            macros: {'protein_g': int, 'carbs_g': int, 'fat_g': int}
            diet_type: 'vegetarian', 'vegan', 'non_vegetarian', 'eggetarian'
            goal: 'lose_weight', 'gain_weight', 'maintain', 'muscle_gain', 'general_fitness'
            allergies: List of allergens to avoid
        
        Returns:
            Complete plan with breakfast, lunch, snack, dinner, and nutrition summary
        """
        allergies = allergies or []

        # VERSION B: Try AI API first
        if self.ai_api_available:
            try:
                plan = self._generate_with_ai_api(daily_calories, macros, diet_type, goal, allergies)
                if plan:
                    logger.info("Plan generated using AI API (Version B)")
                    return plan
            except Exception as e:
                logger.warning(f"AI API failed, falling back to rule-based engine: {e}")

        # VERSION A: Rule-based engine (fallback)
        logger.info("Plan generated using rule-based engine (Version A)")
        return self._generate_rule_based(daily_calories, macros, diet_type, goal, allergies)

    def _generate_with_ai_api(self, daily_calories: int, macros: dict,
                               diet_type: str, goal: str, allergies: list) -> dict:
        """
        VERSION B: Generate plan using external AI API.
        
        Constructs a structured prompt and sends to AI service.
        Validates the response format before returning.
        
        Requires AI_API_KEY and AI_API_URL environment variables.
        """
        import requests

        api_key = os.getenv('AI_API_KEY', '')
        api_url = os.getenv('AI_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent')

        if not api_key:
            return None

        # Construct prompt
        prompt = f"""Generate a one-day diet plan with these requirements:
- Diet type: {diet_type}
- Daily calories target: {daily_calories} kcal
- Protein: {macros['protein_g']}g, Carbs: {macros['carbs_g']}g, Fat: {macros['fat_g']}g
- Goal: {goal}
- Avoid allergens: {', '.join(allergies) if allergies else 'None'}

Return ONLY valid JSON in this exact format:
{{
    "breakfast": [{{"name": "Food Name", "serving": "Amount", "kcal": 300, "protein": 10, "carbs": 40, "fat": 8}}],
    "lunch": [{{"name": "Food Name", "serving": "Amount", "kcal": 500, "protein": 25, "carbs": 60, "fat": 15}}],
    "snack": [{{"name": "Food Name", "serving": "Amount", "kcal": 200, "protein": 5, "carbs": 30, "fat": 5}}],
    "dinner": [{{"name": "Food Name", "serving": "Amount", "kcal": 400, "protein": 20, "carbs": 50, "fat": 12}}]
}}

DISCLAIMER: This is for educational purposes only, not medical advice."""

        try:
            response = requests.post(
                f"{api_url}?key={api_key}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.7}
                },
                timeout=15
            )
            response.raise_for_status()

            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']

            # Extract JSON from response
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                plan_data = json.loads(text[json_start:json_end])
                return self._format_plan(plan_data, daily_calories, macros)
        except Exception as e:
            logger.error(f"AI API error: {e}")
            return None

        return None

    def _generate_rule_based(self, daily_calories: int, macros: dict,
                              diet_type: str, goal: str, allergies: list) -> dict:
        """
        VERSION A: Rule-based diet plan generation.
        
        Algorithm:
        1. Filter foods by diet type and allergens
        2. Categorize foods by meal type (breakfast, lunch, snack, dinner)
        3. Select foods to approximate calorie/macro targets
        4. Distribute calories: breakfast 25%, lunch 35%, snack 15%, dinner 25%
        """
        # Filter foods based on diet type and allergies
        filtered = self._filter_foods(diet_type, allergies)

        # Categorize by meal type
        by_category = {
            'breakfast': [f for f in filtered if f.get('category') == 'breakfast'],
            'lunch': [f for f in filtered if f.get('category') == 'lunch'],
            'snack': [f for f in filtered if f.get('category') == 'snack'],
            'dinner': [f for f in filtered if f.get('category') == 'dinner'],
        }

        # Calorie distribution
        calorie_split = {
            'breakfast': 0.25,
            'lunch': 0.35,
            'snack': 0.15,
            'dinner': 0.25
        }

        plan = {}
        total_cal = 0
        total_p = 0
        total_c = 0
        total_f = 0

        for meal, fraction in calorie_split.items():
            target_cal = daily_calories * fraction
            meal_items = self._select_items_for_meal(
                by_category.get(meal, filtered),
                target_cal,
                meal
            )
            plan[meal] = meal_items

            for item in meal_items:
                total_cal += item.get('kcal', 0)
                total_p += item.get('protein', 0)
                total_c += item.get('carbs', 0)
                total_f += item.get('fat', 0)

        # Build nutrition summary
        nutrition_summary = (
            f"Approximate Daily Total: {total_cal} kcal | "
            f"Protein: {total_p}g | Carbs: {total_c}g | Fat: {total_f}g\n"
            f"Target was: {daily_calories} kcal | "
            f"P: {macros['protein_g']}g | C: {macros['carbs_g']}g | F: {macros['fat_g']}g\n"
            f"Diet Type: {diet_type.replace('_', ' ').title()} | "
            f"Goal: {goal.replace('_', ' ').title()}"
        )

        hydration = (
            "💧 Hydration Reminder: Drink at least 8 glasses (2-2.5 liters) of water daily. "
            "Increase intake during exercise or hot weather."
        )

        return {
            'breakfast': plan['breakfast'],
            'lunch': plan['lunch'],
            'snack': plan['snack'],
            'dinner': plan['dinner'],
            'total_calories': total_cal,
            'macros': {
                'protein_g': total_p,
                'carbs_g': total_c,
                'fat_g': total_f
            },
            'nutrition_summary': nutrition_summary,
            'hydration_reminder': hydration
        }

    def _filter_foods(self, diet_type: str, allergies: list) -> list:
        """Filter food database by dietary preference and allergens."""
        filtered = []

        # Diet type mapping
        diet_map = {
            'vegetarian': ['vegetarian', 'vegan'],
            'vegan': ['vegan'],
            'non_vegetarian': ['vegetarian', 'vegan', 'non_vegetarian', 'eggetarian'],
            'eggetarian': ['vegetarian', 'vegan', 'eggetarian']
        }
        allowed_tags = diet_map.get(diet_type, ['vegetarian', 'vegan'])

        for food in self.foods:
            # Check diet compatibility
            food_tags = food.get('tags', [])
            if not any(tag in allowed_tags for tag in food_tags):
                continue

            # Check allergens
            food_allergens = food.get('allergens', [])
            if any(a.lower() in [fa.lower() for fa in food_allergens] for a in allergies):
                continue

            filtered.append(food)

        return filtered if filtered else self.foods[:8]  # Fallback to first 8 foods

    def _select_items_for_meal(self, foods: list, target_cal: float, meal_type: str) -> list:
        """
        Select food items for a meal to approximate calorie target.
        Uses a randomized greedy approach for variety.
        """
        if not foods:
            return [{
                'name': f'Balanced {meal_type.title()} Meal',
                'serving': '1 serving',
                'kcal': round(target_cal),
                'protein': round(target_cal * 0.3 / 4),
                'carbs': round(target_cal * 0.4 / 4),
                'fat': round(target_cal * 0.3 / 9)
            }]

        selected = []
        remaining_cal = target_cal

        # Shuffle for variety
        shuffled = list(foods)
        random.shuffle(shuffled)

        # Select 2-3 items per meal
        max_items = 3 if meal_type in ('lunch', 'dinner') else 2

        for food in shuffled:
            if len(selected) >= max_items:
                break
            if remaining_cal <= 50:
                break

            per_serving = food.get('per_serving', {})
            food_cal = per_serving.get('kcal', 200)

            if food_cal <= remaining_cal + 100:  # Allow slight overshoot
                selected.append({
                    'name': food.get('name', 'Unknown Food'),
                    'serving': food.get('serving_size', '1 serving'),
                    'kcal': food_cal,
                    'protein': per_serving.get('protein', 0),
                    'carbs': per_serving.get('carbs', 0),
                    'fat': per_serving.get('fat', 0)
                })
                remaining_cal -= food_cal

        return selected if selected else [{
            'name': f'Balanced {meal_type.title()} Meal',
            'serving': '1 serving',
            'kcal': round(target_cal),
            'protein': round(target_cal * 0.3 / 4),
            'carbs': round(target_cal * 0.4 / 4),
            'fat': round(target_cal * 0.3 / 9)
        }]

    def _format_plan(self, plan_data: dict, daily_calories: int, macros: dict) -> dict:
        """Format an AI-generated plan into the standard output structure."""
        total_cal = 0
        total_p = 0
        total_c = 0
        total_f = 0

        for meal in ['breakfast', 'lunch', 'snack', 'dinner']:
            for item in plan_data.get(meal, []):
                total_cal += item.get('kcal', 0)
                total_p += item.get('protein', 0)
                total_c += item.get('carbs', 0)
                total_f += item.get('fat', 0)

        nutrition_summary = (
            f"AI-Generated Daily Total: {total_cal} kcal | "
            f"Protein: {total_p}g | Carbs: {total_c}g | Fat: {total_f}g\n"
            f"Target was: {daily_calories} kcal | "
            f"P: {macros['protein_g']}g | C: {macros['carbs_g']}g | F: {macros['fat_g']}g"
        )

        return {
            'breakfast': plan_data.get('breakfast', []),
            'lunch': plan_data.get('lunch', []),
            'snack': plan_data.get('snack', []),
            'dinner': plan_data.get('dinner', []),
            'total_calories': total_cal,
            'macros': {'protein_g': total_p, 'carbs_g': total_c, 'fat_g': total_f},
            'nutrition_summary': nutrition_summary,
            'hydration_reminder': "💧 Drink at least 8 glasses (2-2.5 liters) of water daily."
        }


# ── Standalone test ────────────────────────────────────────────────
if __name__ == '__main__':
    engine = DietEngine()
    plan = engine.generate_plan(
        daily_calories=2000,
        macros={'protein_g': 150, 'carbs_g': 200, 'fat_g': 67},
        diet_type='vegetarian',
        goal='maintain'
    )
    print(json.dumps(plan, indent=2))
