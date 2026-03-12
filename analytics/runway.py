def calculate_runway(funding_raised: float, burn_rate: float) -> float | None:
    """
    Calculate how many months of runway a startup has left.
    Formula: runway_months = funding_raised / burn_rate

    Returns:
        - Number of months as float
        - None if burn_rate is 0 (no spending = infinite runway)
    """
    if burn_rate is None or burn_rate == 0:
        return None  # infinite runway — no burn

    if funding_raised is None or funding_raised <= 0:
        return 0.0   # no funding left

    return round(funding_raised / burn_rate, 1)


def get_runway_status(runway_months: float | None) -> dict:
    """
    Return a risk label and alert message based on runway length.

    Returns a dict with:
        - status: "safe" | "warning" | "critical"
        - label:  human-readable string
        - alert:  True/False whether to show a banner
    """
    if runway_months is None:
        return {"status": "safe", "label": "Infinite runway", "alert": False}

    if runway_months < 3:
        return {"status": "critical", "label": f"⛔ {runway_months}m runway", "alert": True}
    elif runway_months < 6:
        return {"status": "warning",  "label": f"⚠️ {runway_months}m runway", "alert": True}
    else:
        return {"status": "safe",     "label": f"✅ {runway_months}m runway", "alert": False}