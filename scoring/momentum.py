"""
Calculates startup momentum — measures acceleration, not just size.
A startup growing faster this month than last month scores higher.
"""

def calculate_momentum(recent_growth: float, previous_growth: float) -> dict:
    """
    Calculate momentum from last two growth values.

    Formula:
        momentum = (recent * 0.6) + (previous * 0.4)

    Returns a dict with:
        - momentum_score : float (raw, can be negative)
        - trend          : "accelerating" | "stable" | "decelerating"
        - label          : human-readable string for dashboard
    """
    momentum = round((recent_growth * 0.6) + (previous_growth * 0.4), 4)

    if recent_growth > previous_growth + 0.05:
        trend = "accelerating"
        label = "🚀 Accelerating"
    elif recent_growth < previous_growth - 0.05:
        trend = "decelerating"
        label = "📉 Decelerating"
    else:
        trend = "stable"
        label = "➡️ Stable"

    return {
        "momentum_score": momentum,
        "trend":          trend,
        "label":          label,
    }


def calculate_momentum_from_series(growth_series: list[float]) -> dict:
    """
    Convenience wrapper — pass the full growth series list,
    automatically picks last two values.
    Returns same dict as calculate_momentum().
    """
    if len(growth_series) < 2:
        return {"momentum_score": 0.0, "trend": "stable", "label": "➡️ Stable"}

    return calculate_momentum(
        recent_growth=growth_series[-1],
        previous_growth=growth_series[-2],
    )