import logging
import random

logger = logging.getLogger(__name__)

def play_slots(bet_amount: float):
    logger.info(f"Playing slots with bet amount {bet_amount}")
    symbols = ["🍒", "🍋", "⭐", "🔔", "💎"]
    result = [random.choice(symbols) for _ in range(3)]

    if len(set(result)) == 1:
        multiplier = 10
    elif len(set(result)) == 2:
        multiplier = 2
    else:
        multiplier = 0

    win_amount = bet_amount * multiplier
    logger.info(f"Slots result: {result}, win amount: {win_amount}")
    return win_amount, result

def play_roulette(bet_amount: float, chosen_color: str):
    logger.info(f"Playing roulette with bet amount {bet_amount} on color {chosen_color}")
    colors = ["red", "black", "green"]
    result = random.choice(colors)

    multipliers = {
        "red": 2,
        "black": 2,
        "green": 14
    }

    win_amount = bet_amount * multipliers[result] if result == chosen_color else 0
    logger.info(f"Roulette result: {result}, win amount: {win_amount}")
    return win_amount, result