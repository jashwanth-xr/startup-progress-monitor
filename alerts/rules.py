"""
Alert rules for startup risk detection.
All functions return a list of alert strings — empty list means no alerts.
"""

def check_runway_alert(runway_months: float | None) -> list[str]:
    alerts = []
    if runway_months is None:
        return alerts
    if runway_months < 3:
        alerts.append(f"⛔ CRITICAL: Only {runway_months} months of runway left")
    elif runway_months < 6:
        alerts.append(f"⚠️ WARNING: Runway below 6 months ({runway_months}m remaining)")
    return alerts


def check_revenue_alert(current_revenue: float, previous_revenue: float) -> list[str]:
    alerts = []
    if previous_revenue <= 0:
        return alerts
    drop = (current_revenue - previous_revenue) / previous_revenue
    if drop <= -0.30:
        pct = round(abs(drop) * 100, 1)
        alerts.append(f"⚠️ WARNING: Revenue declining rapidly ({pct}% drop this month)")
    return alerts


def check_burn_rate_alert(current_burn: float, previous_burn: float) -> list[str]:
    alerts = []
    if previous_burn <= 0:
        return alerts
    increase = (current_burn - previous_burn) / previous_burn
    if increase >= 0.50:
        pct = round(increase * 100, 1)
        alerts.append(f"⛔ CRITICAL: Burn rate spike ({pct}% increase this month)")
    return alerts


def run_all_alerts(
    runway_months:    float | None,
    current_revenue:  float,
    previous_revenue: float,
    current_burn:     float,
    previous_burn:    float,
) -> list[str]:
    """
    Run all alert rules and return combined list.
    Empty list = startup is healthy, no warnings.
    """
    alerts = []
    alerts += check_runway_alert(runway_months)
    alerts += check_revenue_alert(current_revenue, previous_revenue)
    alerts += check_burn_rate_alert(current_burn, previous_burn)
    return alerts