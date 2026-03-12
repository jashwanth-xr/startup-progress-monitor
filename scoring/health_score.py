"""
Calculates a startup health score between 0 and 100.
Inputs are growth rates (decimals e.g. 0.2 = 20%) and runway months.
"""

WEIGHTS = {
    "revenue_growth":  0.35,
    "user_growth":     0.30,
    "employee_growth": 0.20,
    "runway":          0.15,
}

def _normalize_growth(growth: float) -> float:
    """
    Convert a growth rate into a 0–100 score.
    - 0%   growth → 50  (neutral)
    - 100% growth → 100 (excellent)
    - -50% decline → 0  (critical)
    Clamps between 0 and 100.
    """
    score = 50 + (growth * 50)
    return max(0.0, min(100.0, score))


def _normalize_runway(runway_months: float | None) -> float:
    """
    Convert runway months into a 0–100 score.
    - 12+ months → 100
    - 6  months  →  50
    - 0  months  →   0
    - None       → 100 (infinite runway)
    """
    if runway_months is None:
        return 100.0
    score = (runway_months / 12) * 100
    return max(0.0, min(100.0, score))


def calculate_health_score(
    revenue_growth:  float,
    user_growth:     float,
    employee_growth: float,
    runway_months:   float | None,
) -> dict:
    """
    Calculate a weighted startup health score between 0 and 100.

    Returns a dict with:
        - score       : float (0–100)
        - grade       : str   (A / B / C / D / F)
        - breakdown   : dict of individual component scores
    """
    r_score  = _normalize_growth(revenue_growth)
    u_score  = _normalize_growth(user_growth)
    e_score  = _normalize_growth(employee_growth)
    rw_score = _normalize_runway(runway_months)

    score = (
        r_score  * WEIGHTS["revenue_growth"]  +
        u_score  * WEIGHTS["user_growth"]     +
        e_score  * WEIGHTS["employee_growth"] +
        rw_score * WEIGHTS["runway"]
    )

    score = round(max(0.0, min(100.0, score)), 1)

    return {
        "score": score,
        "grade": _grade(score),
        "breakdown": {
            "revenue_score":  round(r_score,  1),
            "user_score":     round(u_score,  1),
            "employee_score": round(e_score,  1),
            "runway_score":   round(rw_score, 1),
        }
    }


def _grade(score: float) -> str:
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "F"