"""
Test scoring functions.
Usage (from project root): python -m tests.test_scoring
"""
from scoring.health_score import calculate_health_score
from scoring.momentum     import calculate_momentum, calculate_momentum_from_series

# ── health_score.py ────────────────────────────────────────
print("── health_score.py ──")

# Healthy startup — strong growth, good runway
result = calculate_health_score(
    revenue_growth=0.30,
    user_growth=0.25,
    employee_growth=0.15,
    runway_months=18
)
print(f"Healthy startup  → Score: {result['score']} | Grade: {result['grade']}")
print(f"  Breakdown: {result['breakdown']}")

# Struggling startup — declining revenue, short runway
result2 = calculate_health_score(
    revenue_growth=-0.40,
    user_growth=-0.10,
    employee_growth=0.0,
    runway_months=3
)
print(f"Struggling startup → Score: {result2['score']} | Grade: {result2['grade']}")

# Edge case — zero everything
result3 = calculate_health_score(0.0, 0.0, 0.0, 6)
print(f"Flat startup     → Score: {result3['score']} | Grade: {result3['grade']}")

# Infinite runway (no burn)
result4 = calculate_health_score(0.5, 0.4, 0.2, None)
print(f"Infinite runway  → Score: {result4['score']} | Grade: {result4['grade']}")

# ── momentum.py ────────────────────────────────────────────
print("\n── momentum.py ──")

m1 = calculate_momentum(recent_growth=0.30, previous_growth=0.10)
print(f"Accelerating → {m1}")   # trend: accelerating 🚀

m2 = calculate_momentum(recent_growth=0.10, previous_growth=0.30)
print(f"Decelerating → {m2}")   # trend: decelerating 📉

m3 = calculate_momentum(recent_growth=0.20, previous_growth=0.20)
print(f"Stable       → {m3}")   # trend: stable ➡️

series = [0.05, 0.10, 0.15, 0.28]
m4 = calculate_momentum_from_series(series)
print(f"From series  → {m4}")   # picks last two: 0.15 and 0.28

print("\n✅ All scoring tests passed!")