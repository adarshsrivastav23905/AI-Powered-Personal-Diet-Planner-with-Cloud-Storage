"""Cloud database simulation utilities.

This file models the role of a managed cloud database and is intended to show
how a real production database would store structured user data.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Any, List


@dataclass
class UserProfile:
    user_id: str
    name: str
    email: str
    age: int
    height_cm: int
    weight_kg: float
    sex: str
    activity_level: str
    dietary_preference: str
    goal: str


class CloudDatabaseService:
    """Very small in-memory simulation of a managed cloud database."""

    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.plans: Dict[str, Dict[str, Any]] = {}

    def save_user_profile(self, profile: UserProfile):
        self.users[profile.user_id] = asdict(profile)

    def get_user_profile(self, user_id: str):
        return self.users.get(user_id)

    def save_plan(self, user_id: str, plan_id: str, plan_data: Dict[str, Any]):
        self.plans[plan_id] = {"user_id": user_id, **plan_data}

    def get_user_plans(self, user_id: str) -> List[Dict[str, Any]]:
        return [plan for plan in self.plans.values() if plan.get("user_id") == user_id]

    def clear(self):
        self.users.clear()
        self.plans.clear()
