"""
Unit tests for dice notation parser.

Tests validate that the parser:
1. Correctly parses valid dice notation
2. Raises clear errors for invalid input (fail-fast)
3. Validates edge cases (zero/negative values)

Run with: pytest tests/test_dice_parser.py -v
"""

import pytest
from utils.dice_parser import parse_hit_dice, parse_damage_dice


# ============================================================================
# Valid Input Tests
# ============================================================================

def test_parse_hit_dice_valid():
    """Test parsing valid hit dice notation."""
    assert parse_hit_dice("18d10") == 10
    assert parse_hit_dice("3d6") == 6
    assert parse_hit_dice("1d8") == 8
    assert parse_hit_dice("12d12") == 12
    assert parse_hit_dice("5d4") == 4
    assert parse_hit_dice("100d20") == 20


def test_parse_damage_dice_with_positive_modifier():
    """Test parsing damage dice with positive modifier."""
    assert parse_damage_dice("1d10+5") == (1, 10, 5)
    assert parse_damage_dice("2d6+3") == (2, 6, 3)
    assert parse_damage_dice("3d8+7") == (3, 8, 7)


def test_parse_damage_dice_no_modifier():
    """Test parsing damage dice without modifier."""
    assert parse_damage_dice("1d6") == (1, 6, 0)
    assert parse_damage_dice("3d8") == (3, 8, 0)
    assert parse_damage_dice("2d12") == (2, 12, 0)


def test_parse_damage_dice_with_negative_modifier():
    """Test parsing damage dice with negative modifier."""
    assert parse_damage_dice("1d4-1") == (1, 4, -1)
    assert parse_damage_dice("2d6-2") == (2, 6, -2)
    assert parse_damage_dice("1d8-3") == (1, 8, -3)


def test_parse_damage_dice_large_values():
    """Test parsing large but valid dice values."""
    assert parse_damage_dice("10d20+15") == (10, 20, 15)
    assert parse_damage_dice("50d100+50") == (50, 100, 50)


# ============================================================================
# Invalid Input Tests (Fail-Fast)
# ============================================================================

def test_parse_hit_dice_invalid_format_raises_error():
    """Test that invalid format raises ValueError with clear message."""
    with pytest.raises(ValueError, match="Invalid hit dice notation"):
        parse_hit_dice("invalid")
    
    with pytest.raises(ValueError, match="Invalid hit dice notation"):
        parse_hit_dice("")
    
    with pytest.raises(ValueError, match="Invalid hit dice notation"):
        parse_hit_dice("abc")


def test_parse_damage_dice_invalid_format_raises_error():
    """Test that invalid format raises ValueError with clear message."""
    with pytest.raises(ValueError, match="Invalid damage dice notation"):
        parse_damage_dice("invalid")
    
    with pytest.raises(ValueError, match="Invalid damage dice notation"):
        parse_damage_dice("")
    
    with pytest.raises(ValueError, match="Invalid damage dice notation"):
        parse_damage_dice("not-dice")


# ============================================================================
# Edge Case Tests (Educational - Validation)
# ============================================================================

def test_parse_hit_dice_zero_dice_raises_error():
    """Test that zero dice count raises ValueError."""
    with pytest.raises(ValueError, match="Number of dice must be positive"):
        parse_hit_dice("0d6")


def test_parse_hit_dice_zero_die_size_raises_error():
    """Test that zero die size raises ValueError."""
    with pytest.raises(ValueError, match="Die size must be positive"):
        parse_hit_dice("3d0")


def test_parse_damage_dice_zero_dice_raises_error():
    """Test that zero dice count raises ValueError."""
    with pytest.raises(ValueError, match="Number of dice must be positive"):
        parse_damage_dice("0d6+3")


def test_parse_damage_dice_zero_die_size_raises_error():
    """Test that zero die size raises ValueError."""
    with pytest.raises(ValueError, match="Die size must be positive"):
        parse_damage_dice("2d0+5")


def test_parse_damage_dice_negative_modifier_is_valid():
    """Test that negative modifiers are allowed (Goblin has STR -1!)."""
    # This should NOT raise an error - negative modifiers are valid
    result = parse_damage_dice("1d6-1")
    assert result == (1, 6, -1)
    
    result = parse_damage_dice("2d8-5")
    assert result == (2, 8, -5)


def test_parse_damage_dice_large_negative_modifier_is_valid():
    """Test that even very negative modifiers are technically valid."""
    # Even if damage would be negative, the modifier itself is valid
    # (the combat system will clamp damage to 0)
    result = parse_damage_dice("1d4-100")
    assert result == (1, 4, -100)


# ============================================================================
# Format Validation Tests
# ============================================================================

def test_parse_hit_dice_requires_d_separator():
    """Test that 'd' separator is required."""
    with pytest.raises(ValueError, match="Invalid hit dice notation"):
        parse_hit_dice("3x6")  # Wrong separator
    
    with pytest.raises(ValueError, match="Invalid hit dice notation"):
        parse_hit_dice("36")  # Missing separator


def test_parse_damage_dice_requires_d_separator():
    """Test that 'd' separator is required."""
    with pytest.raises(ValueError, match="Invalid damage dice notation"):
        parse_damage_dice("2x6+3")  # Wrong separator
    
    with pytest.raises(ValueError, match="Invalid damage dice notation"):
        parse_damage_dice("26+3")  # Missing separator


