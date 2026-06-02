"""Meal planning algorithm: assigns recipes based on calendar appointments."""

import random
from datetime import date

from .recipes import (
    NON_VEGETARIAN,
    QUICK_VEGETARIAN,
    VEGETARIAN,
    Recipe,
)

MAX_NON_VEGETARIAN_PER_WEEK = 2


def plan_week(schedule: dict[date, bool]) -> dict[date, Recipe]:
    """Assign one recipe per day, respecting constraints.

    Constraints:
    - Days with appointments → quick recipes only (prep ≤ 15 min)
    - At most MAX_NON_VEGETARIAN_PER_WEEK non-vegetarian meals
    - No repeated recipes in the same week
    - Deterministic per week number (same plan if re-run on same week)
    """
    dates = sorted(schedule.keys())
    week_number = dates[0].isocalendar()[1]
    rng = random.Random(week_number + dates[0].year * 100)

    used_ids: set[str] = set()
    plan: dict[date, Recipe] = {}
    non_veg_count = 0

    # Pre-select which days get non-vegetarian (prefer days without appointments)
    non_appointment_days = [d for d in dates if not schedule[d]]
    non_veg_days: set[date] = set()

    non_veg_candidates = rng.sample(
        non_appointment_days,
        min(MAX_NON_VEGETARIAN_PER_WEEK, len(non_appointment_days)),
    )
    non_veg_days = set(non_veg_candidates[:MAX_NON_VEGETARIAN_PER_WEEK])

    for day in dates:
        has_appointment = schedule[day]

        if has_appointment:
            pool = [r for r in QUICK_VEGETARIAN if r.id not in used_ids]
            if not pool:
                pool = [r for r in VEGETARIAN if r.id not in used_ids]
        elif day in non_veg_days and non_veg_count < MAX_NON_VEGETARIAN_PER_WEEK:
            pool = [r for r in NON_VEGETARIAN if r.id not in used_ids]
            if not pool:
                pool = [r for r in VEGETARIAN if r.id not in used_ids]
        else:
            pool = [r for r in VEGETARIAN if r.id not in used_ids]
            if not pool:
                pool = [r for r in QUICK_VEGETARIAN if r.id not in used_ids]

        if not pool:
            from .recipes import RECIPES
            pool = [r for r in RECIPES if r.id not in used_ids] or RECIPES

        chosen = rng.choice(pool)
        plan[day] = chosen
        used_ids.add(chosen.id)
        if not chosen.is_vegetarian:
            non_veg_count += 1

    return plan
