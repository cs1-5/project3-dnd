"""
Dice rolling utilities for D&D combat simulation.

This module provides functions for rolling dice with various configurations.

PHASE 1 TODO: Implement these three functions to handle randomness in combat.
You'll need to import the `random` module and use random.randint().
"""

# TODO: Import the random module here


def roll_d20() -> int:
    """
    Roll a single 20-sided die (d20).
    
    Returns:
        Random integer between 1 and 20 (inclusive)
    
    Examples:
        roll_d20()  # Should return random value from 1 to 20
    
    TODO: Implement this function
    Hint: Use random.randint(1, 20)
    """
    return 10  # DUMMY VALUE - Replace with actual implementation


def roll_dice(num_dice: int, die_size: int) -> list[int]:
    """
    Roll multiple dice and return individual results.
    
    Args:
        num_dice: Number of dice to roll
        die_size: Size of each die (e.g., 6 for d6, 8 for d8)
    
    Returns:
        List of individual dice rolls
    
    Examples:
        roll_dice(2, 6)   # Should return something like [3, 5]
        roll_dice(1, 20)  # Should return something like [14]
        roll_dice(3, 8)   # Should return something like [2, 7, 8]
    
    TODO: Implement this function
    Hint: Use a list comprehension with random.randint(1, die_size)
    Hint: You need to repeat the roll num_dice times
    """
    return [3] * num_dice  # DUMMY VALUE - Replace with actual implementation


def roll_with_modifier(num_dice: int, die_size: int, modifier: int) -> tuple[int, list[int]]:
    """
    Roll dice with a modifier and return both total and individual rolls.
    
    Args:
        num_dice: Number of dice to roll
        die_size: Size of each die
        modifier: Flat modifier to add to the total (can be negative)
    
    Returns:
        Tuple of (total_damage, individual_rolls)
        - total_damage: Sum of rolls + modifier (minimum 0)
        - individual_rolls: List of individual dice results
    
    Examples:
        roll_with_modifier(2, 6, 3)   # Might return (12, [4, 5]) - rolls sum to 9, +3 = 12
        roll_with_modifier(1, 8, -1)  # Might return (2, [3]) - rolled 3, -1 = 2
        roll_with_modifier(3, 4, 0)   # Might return (7, [2, 3, 2]) - no modifier
    
    TODO: Implement this function
    Hint: First call roll_dice() to get the individual rolls
    Hint: Calculate total = sum(rolls) + modifier
    Hint: Use max(0, total) to ensure damage can't be negative
    Hint: Return a tuple: (total, rolls)
    """
    rolls = [3] * num_dice  # DUMMY VALUE
    total = sum(rolls) + modifier
    return (max(0, total), rolls)  # PARTIALLY CORRECT - Update to use actual rolls

