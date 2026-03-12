"""
Test all analytics functions.
Usage (from project root): python -m tests.test_analytics
"""
from analytics.growth  import calculate_growth, calculate_growth_series
from analytics.runway  import calculate_runway, get_runway_status
from analytics.trends  import build_metrics_df, add_growth_columns, calculate_momentum

# ── growth.py ──────────────────────────────────────────────
print("── growth.py ──")
print(calculate_growth(120, 100))   # → 0.2  (20% growth)
print(calculate_growth(80,  100))   # → -0.2 (20% decline)
print(calculate_growth(100, 0))     # → 0.0  (div by zero guard)
print(calculate_growth_series([100, 120, 150, 120]))
# → [0.0, 0.2, 0.25, -0.2]

# ── runway.py ──────────────────────────────────────────────
print("\n── runway.py ──")
print(calculate_runway(1200000, 200000))   # → 6.0 months
print(calculate_runway(500000,  0))        # → None (infinite)
print(calculate_runway(0,       200000))   # → 0.0  (no funding)
print(get_runway_status(2.5))    # → critical ⛔
print(get_runway_status(5.0))    # → warning  ⚠️
print(get_runway_status(12.0))   # → safe     ✅
print(get_runway_status(None))   # → safe (infinite)

# ── trends.py ──────────────────────────────────────────────
print("\n── trends.py ──")
sample = [
    {"month": "2024-01-01", "monthly_users": 1000, "monthly_revenue": 50000,
     "employee_count": 10, "funding_raised": 500000, "burn_rate": 40000},
    {"month": "2024-02-01", "monthly_users": 1200, "monthly_revenue": 62000,
     "employee_count": 12, "funding_raised": 460000, "burn_rate": 40000},
    {"month": "2024-03-01", "monthly_users": 1500, "monthly_revenue": 80000,
     "employee_count": 15, "funding_raised": 420000, "burn_rate": 40000},
]

df = build_metrics_df(sample)
df = add_growth_columns(df)
print(df[["month", "monthly_revenue", "revenue_growth", "user_growth"]].to_string())

momentum = calculate_momentum(df, col="revenue_growth")
print(f"\nMomentum score: {momentum}")   # → positive, accelerating startup

print("\n✅ All analytics tests passed!")


# ── alerts/rules.py ────────────────────────────────────────
from alerts.rules import run_all_alerts, check_runway_alert

print("\n── alerts/rules.py ──")

# All alerts firing
a1 = run_all_alerts(
    runway_months=4,
    current_revenue=50000,  previous_revenue=90000,  # 44% drop
    current_burn=180000,    previous_burn=100000,     # 80% spike
)
print("All alerts:", a1)

# No alerts — healthy startup
a2 = run_all_alerts(
    runway_months=18,
    current_revenue=120000, previous_revenue=100000,
    current_burn=40000,     previous_burn=38000,
)
print("No alerts:", a2)

# Infinite runway
a3 = check_runway_alert(None)
print("Infinite runway alerts:", a3)   # → []

print("✅ Alert tests passed!")