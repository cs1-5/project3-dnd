"""
Probability Calculator for D&D 5e Combat
Core probability functions for teaching discrete mathematics and probability.
"""


# PHASE 2 TODO: Implement this probability calculation
# Formula: P(hit) = (21 - (AC - attack_bonus)) / 20
# Note: Clamped between 0.05 (always 5% chance on natural 1) and 0.95 (always 5% miss chance on natural 20)
def calculate_hit_probability(attack_bonus: int, target_ac: int) -> float:
    """
    Calculate the probability of an attack hitting in D&D 5e.
    
    Args:
        attack_bonus: The attacker's attack bonus (ability modifier + proficiency)
        target_ac: The target's Armor Class
    
    Returns:
        Probability of hitting as a float between 0.0 and 1.0
    
    Examples:
        calculate_hit_probability(5, 15)   # Returns: 0.55 (need 10+ on d20)
        calculate_hit_probability(0, 20)   # Returns: 0.05 (need nat 20)
        calculate_hit_probability(15, 10)  # Returns: 0.95 (auto-hit except nat 1)
    
    TODO: Implement this function using the formula provided above.
    Hint: Calculate needed_roll = target_ac - attack_bonus
    Hint: If needed_roll <= 1, return 0.95 (95% hit, 5% auto-miss)
    Hint: If needed_roll >= 20, return 0.05 (5% auto-hit)
    Hint: Otherwise, return (21 - needed_roll) / 20
    """
    return 0.5  # DUMMY VALUE - Replace with actual implementation


# PHASE 2 TODO: Calculate expected value of dice rolls
# Formula: E(XdY + M) = X * (Y + 1) / 2 + M
# For example: E(2d6 + 3) = 2 * (6 + 1) / 2 + 3 = 2 * 3.5 + 3 = 10
def calculate_expected_damage(num_dice: int, die_size: int, modifier: int) -> float:
    """
    Calculate expected (average) damage from dice rolls.
    
    Args:
        num_dice: Number of dice to roll
        die_size: Size of each die (e.g., 6 for d6, 20 for d20)
        modifier: Flat modifier added to the roll
    
    Returns:
        Expected damage as a float
    
    Examples:
        calculate_expected_damage(1, 8, 4)  # Returns: 8.5 (1d8+4 avg)
        calculate_expected_damage(2, 6, 0)  # Returns: 7.0 (2d6 avg)
        calculate_expected_damage(1, 4, -1) # Returns: 1.5 (1d4-1 avg)
    
    TODO: Implement this function using the formula provided above.
    Hint: Calculate expected_per_die = (1 + die_size) / 2
    Hint: For d8: (1 + 8) / 2 = 4.5
    Hint: Total expected = num_dice * expected_per_die + modifier
    """
    return 5.0  # DUMMY VALUE - Replace with actual implementation


# PHASE 2 TODO: Calculate critical hit probability
# Formula: P(crit) = 1 / 20 = 0.05 for a standard d20
def calculate_crit_probability() -> float:
    """
    Calculate the probability of rolling a critical hit (natural 20) on a d20.
    
    Returns:
        Probability as a float (always 0.05 for standard d20)
    
    Examples:
        calculate_crit_probability()  # Returns: 0.05 (always 5% or 1/20)
    
    NOTE: This one is already implemented for you as an example!
    """
    # In D&D 5e, only a natural 20 is a critical hit
    # Probability = 1 success outcome / 20 possible outcomes
    return 1 / 20  # Already correct - use this as a reference!


# PHASE 2 TODO: Calculate minimum roll needed
def calculate_min_roll_needed(attack_bonus: int, target_ac: int) -> int:
    """
    Calculate the minimum d20 roll needed to hit (before auto-hit/miss rules).
    
    This returns the theoretical minimum roll needed, but note:
    - Natural 1 always misses (auto-miss)
    - Natural 20 always hits (auto-hit)
    
    Args:
        attack_bonus: The attacker's attack bonus
        target_ac: The target's Armor Class
    
    Returns:
        Minimum d20 roll needed (1-20), clamped to valid range
        - Returns 1 if very easy to hit (even though nat 1 still misses)
        - Returns 20 if requires natural 20 to hit
    
    Examples:
        calculate_min_roll_needed(10, 10)  # Returns: 1 (very easy, but nat 1 still misses!)
        calculate_min_roll_needed(5, 15)   # Returns: 10 (need 10+ on d20)
        calculate_min_roll_needed(0, 20)   # Returns: 20 (only nat 20 hits)
    
    TODO: Implement this function
    Hint: Calculate needed = target_ac - attack_bonus
    Hint: Use max() and min() to clamp between 1 and 20
    Hint: return max(1, min(20, needed))
    """
    return 10  # DUMMY VALUE - Replace with actual implementation


# PHASE 2 TODO: Calculate damage range
def calculate_damage_range(num_dice: int, die_size: int, modifier: int) -> tuple[int, int]:
    """
    Calculate the minimum and maximum possible damage.
    
    Args:
        num_dice: Number of dice to roll
        die_size: Size of each die
        modifier: Flat modifier
    
    Returns:
        Tuple of (min_damage, max_damage)
    
    Examples:
        calculate_damage_range(1, 8, 3)   # Returns: (4, 11) for 1d8+3
        calculate_damage_range(2, 6, 0)   # Returns: (2, 12) for 2d6
        calculate_damage_range(1, 4, -1)  # Returns: (0, 3) for 1d4-1 (min clamped to 0)
    
    TODO: Implement this function
    Hint: Min damage = num_dice * 1 + modifier (all dice roll minimum)
    Hint: Max damage = num_dice * die_size + modifier (all dice roll maximum)
    Hint: Use max(0, ...) to ensure damage can't be negative
    Hint: Return tuple: (max(0, min_damage), max(0, max_damage))
    """
    return (1, 10)  # DUMMY VALUE - Replace with actual implementation


# PHASE 3 TODO: Conditional Probability - P(A | B)
# Formula: P(crit | hit) = P(crit AND hit) / P(hit) = P(crit) / P(hit)
# This is DIFFERENT from P(crit) alone!
def calculate_crit_given_hit(attack_bonus: int, target_ac: int) -> float:
    """
    Calculate the conditional probability of a critical hit GIVEN that you hit.
    This demonstrates conditional probability: P(crit | hit)
    
    In D&D 5e, every critical hit (natural 20) is also a hit, so:
    P(crit | hit) = P(crit AND hit) / P(hit) = P(crit) / P(hit)
    
    Args:
        attack_bonus: The attacker's attack bonus
        target_ac: The target's Armor Class
    
    Returns:
        Probability of critical hit given that the attack hit (0.0 to 1.0)
    
    Examples:
        calculate_crit_given_hit(5, 15)   # Returns: ~0.0909 (9.09% crit | hit)
                                          # (55% hit rate, so 5% / 55% = 9.09%)
        
        calculate_crit_given_hit(0, 18)   # Returns: ~0.333 (33.3% crit | hit)
                                          # (Only 15% hit rate, so 5% / 15% = 33.3%)
        
    Note: This is HIGHER than the raw 5% crit rate because we're conditioning
    on the fact that we already know the attack hit!
    
    TODO: Implement this function using the conditional probability formula above.
    Hint: Use calculate_crit_probability() and calculate_hit_probability()
    Hint: In D&D, every crit is also a hit, so P(crit AND hit) = P(crit)
    """
    return 0.1  # DUMMY VALUE - Replace with actual implementation


# PHASE 3 TODO: Expected damage including miss chance
# Formula: E[damage per attack] = P(hit) × E[damage | hit]
# This accounts for the fact that you might miss entirely!
def calculate_expected_damage_per_attack(
    attack_bonus: int, 
    target_ac: int,
    num_dice: int, 
    die_size: int, 
    modifier: int
) -> float:
    """
    Calculate expected damage per attack, accounting for the chance to miss.
    
    This is different from calculate_expected_damage(), which gives the expected
    damage IF you roll the dice. This function accounts for missing entirely.
    
    Args:
        attack_bonus: The attacker's attack bonus
        target_ac: The target's Armor Class
        num_dice: Number of dice to roll for damage
        die_size: Size of each die
        modifier: Flat modifier added to damage
    
    Returns:
        Expected damage per attack as a float
    
    Examples:
        calculate_expected_damage_per_attack(5, 15, 1, 8, 3)
        # Returns: ~4.125 (55% hit × 7.5 avg damage)
        
        calculate_expected_damage_per_attack(0, 20, 2, 6, 0)
        # Returns: ~0.35 (5% hit × 7.0 avg damage)
    
    Note: This is the "true" expected damage when you declare an attack,
    including the possibility of missing!
    
    TODO: Implement this function by combining hit probability with expected damage.
    Hint: Use calculate_hit_probability() and calculate_expected_damage()
    Hint: Consider what happens when you miss (0 damage)
    """
    return 2.0  # DUMMY VALUE - Replace with actual implementation

