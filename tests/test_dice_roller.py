"""
Tests for dice_roller.py - PHASE 1

Students: Write tests to verify your dice rolling implementations work correctly.
"""

import pytest
from utils.dice_roller import roll_d20, roll_dice, roll_with_modifier


class TestRollD20:
    """Tests for the roll_d20() function."""
    
    def test_roll_d20_returns_int(self):
        """Test that roll_d20 returns an integer."""
        result = roll_d20()
        assert isinstance(result, int)
    
    # TODO: Add more tests for roll_d20
    # Suggested tests:
    # - Test that result is in range 1-20
    # - Test that calling it multiple times gives different results (randomness)
    # - Test rolling 100 times and verify all results are in valid range


class TestRollDice:
    """Tests for the roll_dice() function."""
    
    def test_roll_dice_returns_list(self):
        """Test that roll_dice returns a list."""
        result = roll_dice(2, 6)
        assert isinstance(result, list)
    
    def test_roll_dice_correct_length(self):
        """Test that roll_dice returns correct number of results."""
        result = roll_dice(3, 6)
        assert len(result) == 3
    
    # TODO: Add more tests for roll_dice
    # Suggested tests:
    # - Test that each die result is in valid range (1 to die_size)
    # - Test with different die sizes (d4, d8, d12, d20)
    # - Test rolling 1 die
    # - Test rolling many dice (e.g., 10d6)


class TestRollWithModifier:
    """Tests for the roll_with_modifier() function."""
    
    def test_roll_with_modifier_returns_tuple(self):
        """Test that roll_with_modifier returns a tuple."""
        result = roll_with_modifier(1, 6, 0)
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_roll_with_modifier_structure(self):
        """Test the structure of returned tuple (total, rolls)."""
        total, rolls = roll_with_modifier(2, 6, 3)
        assert isinstance(total, int)
        assert isinstance(rolls, list)
        assert len(rolls) == 2
    
    # TODO: Add more tests for roll_with_modifier
    # Suggested tests:
    # - Test that total = sum(rolls) + modifier
    # - Test with positive modifier
    # - Test with negative modifier
    # - Test that minimum damage is 0 (even with large negative modifier)
    # - Test with modifier = 0


# BONUS TODO (Optional): Statistical Testing
# Write a test that rolls dice many times (e.g., 1000) and verifies
# that the average is close to the expected value.
# For example: rolling 1d20 1000 times should average close to 10.5
#
# Example skeleton:
# def test_d20_statistical_average():
#     rolls = [roll_d20() for _ in range(1000)]
#     average = sum(rolls) / len(rolls)
#     # Expected average of d20 is 10.5
#     # Allow some variance (e.g., between 10.0 and 11.0)
#     assert 10.0 <= average <= 11.0

