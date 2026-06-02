"""Shopping list generator: aggregates ingredients by category."""

from datetime import date

from .recipes import CATEGORIES, Ingredient, Recipe

CATEGORY_ORDER = [
    "verdure",
    "latticini",
    "legumi",
    "carne_pesce",
    "pasta_riso",
    "pane",
    "dispensa",
]


def build_shopping_list(
    plan: dict[date, Recipe],
) -> dict[str, list[tuple[str, str]]]:
    """Return ingredients grouped by category, with quantities merged where possible.

    Returns: {category_key: [(ingredient_name, quantity), ...]}
    """
    aggregated: dict[str, dict[str, list[str]]] = {c: {} for c in CATEGORIES}

    for recipe in plan.values():
        for ing in recipe.ingredients:
            cat = ing.category if ing.category in aggregated else "dispensa"
            if ing.name not in aggregated[cat]:
                aggregated[cat][ing.name] = []
            aggregated[cat][ing.name].append(ing.quantity)

    result: dict[str, list[tuple[str, str]]] = {}
    for cat in CATEGORY_ORDER:
        items = aggregated.get(cat, {})
        if items:
            result[cat] = [
                (name, _merge_quantities(qtys)) for name, qtys in sorted(items.items())
            ]

    return result


def _merge_quantities(quantities: list[str]) -> str:
    """Merge duplicate quantities into a readable string."""
    if len(quantities) == 1:
        return quantities[0]
    unique = list(dict.fromkeys(quantities))
    if len(unique) == 1:
        return f"{len(quantities)}x {unique[0]}"
    return " + ".join(quantities)
