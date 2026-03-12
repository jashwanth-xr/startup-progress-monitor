def calculate_growth(current_value: float, previous_value: float) -> float:
    """
    Calculate growth rate between two periods.
    Formula: (current - previous) / previous
    Returns 0 if previous_value is zero to avoid division by zero.
    """
    if previous_value == 0 or previous_value is None:
        return 0.0
    return (current_value - previous_value) / previous_value


def calculate_growth_series(values: list) -> list:
    """
    Calculate month-over-month growth for a list of values.
    Returns a list of growth rates (first element is always 0.0).
    Works for revenue, users, or employee counts.

    Example:
        values = [100, 120, 150]
        returns [0.0, 0.20, 0.25]
    """
    if not values or len(values) < 2:
        return [0.0] * len(values)

    growth_rates = [0.0]  # no previous value for first month
    for i in range(1, len(values)):
        rate = calculate_growth(values[i], values[i - 1])
        growth_rates.append(rate)

    return growth_rates