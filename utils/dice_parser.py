"""
Dice notation parser for D&D combat.

Parses dice notation like "18d10", "2d6+5", etc.
Validates input and raises clear errors for educational purposes.
"""

import re


def parse_hit_dice(hit_dice_str: str) -> int:
    """
    Parse hit dice to extract die size.
    
    Args:
        hit_dice_str: Hit dice notation like "18d10" or "3d6"
    
    Returns:
        Die size as integer (e.g., 10, 6, 8)
    
    Raises:
        ValueError: If the dice notation is invalid or die size is not positive
    
    Examples:
        parse_hit_dice("18d10")  # Returns: 10
        parse_hit_dice("3d6")    # Returns: 6
        parse_hit_dice("1d8")    # Returns: 8
    """
    match = re.search(r'(\d+)d(\d+)', hit_dice_str)
    
    if not match:
        raise ValueError(
            f"Invalid hit dice notation: '{hit_dice_str}'. "
            f"Expected format: 'NdS' (e.g., '3d6', '18d10')"
        )
    
    num_dice = int(match.group(1))
    die_size = int(match.group(2))
    
    # Validate that values are positive
    if num_dice < 1:
        raise ValueError(f"Number of dice must be positive, got {num_dice}")
    if die_size < 1:
        raise ValueError(f"Die size must be positive, got {die_size}")
    
    return die_size


def parse_damage_dice(damage_str: str) -> tuple[int, int, int]:
    """
    Parse damage dice notation into components.
    
    Args:
        damage_str: Dice notation like "1d10+5" or "2d6-1"
    
    Returns:
        Tuple of (num_dice, die_size, modifier)
    
    Raises:
        ValueError: If the dice notation is invalid or values are not positive
    
    Examples:
        parse_damage_dice("1d10+5")  # Returns: (1, 10, 5)
        parse_damage_dice("2d6")     # Returns: (2, 6, 0)
        parse_damage_dice("1d4-1")   # Returns: (1, 4, -1)
    """
    match = re.search(r'(\d+)d(\d+)([+-]\d+)?', damage_str)
    
    if not match:
        raise ValueError(
            f"Invalid damage dice notation: '{damage_str}'. "
            f"Expected format: 'NdS' or 'NdS+M' (e.g., '2d6', '1d10+5', '1d4-1')"
        )
    
    num_dice = int(match.group(1))
    die_size = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    # Validate that dice count and size are positive
    if num_dice < 1:
        raise ValueError(f"Number of dice must be positive, got {num_dice}")
    if die_size < 1:
        raise ValueError(f"Die size must be positive, got {die_size}")
    
    return (num_dice, die_size, modifier)


