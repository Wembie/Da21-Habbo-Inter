def calculate_tip(game_amount: float) -> float:
    """Calculate tip for Habbo credits."""
    if 5.0 <= game_amount < 10.0:
        return 2.0
    elif 10.0 <= game_amount < 15.0:
        return 3.0
    elif 15.0 <= game_amount < 20.0:
        return 4.0
    elif 20.0 <= game_amount < 26.0:
        return 5.0
    elif 26.0 <= game_amount < 31.0:
        return 6.0
    elif 31.0 <= game_amount < 36.0:
        return 7.0
    elif 36.0 <= game_amount < 41.0:
        return 8.0
    elif 41.0 <= game_amount < 50.0:
        return 9.0
    elif 50.0 <= game_amount < 100.0:
        return 10.0
    elif 100.0 <= game_amount < 150.0:
        return 20.0
    elif 150.0 <= game_amount < 500.0:
        return 30.0
    else:
        return round(50.0 * (game_amount // 500.0), 2)


def calculate_tip_usdt(game_amount: float) -> float:
    """Calculate tip for USDT."""
    if 1.0 <= game_amount < 10.0:
        return 0.5
    return round(game_amount // 10.0, 2)
