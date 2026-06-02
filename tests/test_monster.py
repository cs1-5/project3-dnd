"""
Tests for the Monster model class.

PHASE 4: Understanding OOP Testing

These tests demonstrate how to test object-oriented code. Your tasks:
1. Read through the tests and understand what each one verifies
2. Fill in the missing TODO assertions (marked with ???)
3. Add 2 simple tests at the end following the existing patterns

Focus on:
- Fail-fast validation (required fields)
- Correct computation of derived attributes  
- Property access returns cached values
"""

import pytest
from models.monster import Monster


class TestMonsterInitialization:
    """Test Monster initialization and validation."""
    
    def test_successful_initialization_with_valid_data(self):
        """Test that a Monster can be created with all required fields."""
        data = {
            "index": "goblin",
            "name": "Goblin",
            "hit_points": 7,
            "armor_class": [{"value": 15}],
            "strength": 8,
            "proficiency_bonus": 2,
            "hit_dice": "2d6",
            "full_image_url": "https://example.com/goblin.png"
        }
        
        monster = Monster(data)
        
        assert monster.index == "goblin"
        assert monster.name == "Goblin"
        assert monster.hp == 7
        assert monster.ac == 15
        assert monster.strength == 8
        assert monster.image_url == "https://example.com/goblin.png"
    
    def test_initialization_with_defaults(self):
        """Test that optional fields use sensible defaults."""
        data = {
            "name": "Test Monster",
            "hit_points": 50,
            "armor_class": [{"value": 12}],
            "strength": 10,
            # No proficiency_bonus, hit_dice, or image_url
        }
        
        monster = Monster(data)
        
        assert monster.index == ""
        assert monster.proficiency_bonus == 2
        assert monster.hit_dice == "1d8"
        assert monster.image_url is None


class TestMonsterValidation:
    """Test fail-fast validation for required fields."""
    
    def test_missing_hit_points_raises_error(self):
        """Test that missing hit_points raises ValueError immediately."""
        data = {
            "name": "Invalid Monster",
            # Missing hit_points
            "armor_class": [{"value": 12}],
            "strength": 10,
        }
        
        with pytest.raises(ValueError, match="missing required 'hit_points'"):
            Monster(data)
    
    def test_missing_armor_class_raises_error(self):
        """Test that missing armor_class raises ValueError immediately."""
        data = {
            "name": "Invalid Monster",
            "hit_points": 50,
            # Missing armor_class
            "strength": 10,
        }
        
        with pytest.raises(ValueError, match="missing required 'armor_class'"):
            Monster(data)
    
    def test_missing_strength_raises_error(self):
        """Test that missing strength raises ValueError immediately."""
        data = {
            "name": "Invalid Monster",
            "hit_points": 50,
            "armor_class": [{"value": 12}],
            # Missing strength
        }
        
        with pytest.raises(ValueError, match="missing required 'strength'"):
            Monster(data)


class TestDerivedAttributes:
    """Test correct computation of derived attributes."""
    
    def test_attack_bonus_calculation(self):
        """Test that attack bonus = STR modifier + proficiency."""
        data = {
            "name": "Strong Monster",
            "hit_points": 50,
            "armor_class": [{"value": 12}],
            "strength": 16,  # Modifier = +3
            "proficiency_bonus": 2,
        }
        
        monster = Monster(data)
        
        # STR 16 -> modifier +3, proficiency +2 -> total +5
        assert monster.attack_bonus == 5
    
    def test_damage_dice_with_positive_modifier(self):
        """Test damage dice notation with positive STR modifier."""
        data = {
            "name": "Strong Monster",
            "hit_points": 50,
            "armor_class": [{"value": 12}],
            "strength": 14,  # Modifier = +2
            "hit_dice": "3d10",
        }
        
        monster = Monster(data)
        
        assert monster.damage_dice == "1d10+2"
        assert monster.damage_dice_parsed == (1, 10, 2)
    
    def test_damage_dice_with_negative_modifier(self):
        """Test damage dice notation with negative STR modifier (like Goblin)."""
        data = {
            "name": "Weak Monster",
            "hit_points": 7,
            "armor_class": [{"value": 15}],
            "strength": 8,  # Modifier = -1
            "hit_dice": "2d6",
        }
        
        monster = Monster(data)
        
        assert monster.damage_dice == "1d6-1"
        assert monster.damage_dice_parsed == (1, 6, -1)


class TestStrengthModifierCalculation:
    """Test D&D 5e ability modifier calculations.
    
    Formula: modifier = (strength - 10) // 2
    Attack bonus = modifier + proficiency_bonus (default 2)
    """
    
    def test_modifier_goblin_strength(self):
        """Test modifier for STR 8 (like a Goblin)."""
        data = {
            "name": "Goblin",
            "hit_points": 7,
            "armor_class": [{"value": 15}],
            "strength": 8,
        }
        monster = Monster(data)
        # STR 8 -> modifier -1, proficiency +2 -> attack bonus +1
        assert monster.attack_bonus == 1
    
    # PHASE 4 TODO: Fill in the expected attack bonus for each test below
    # Use the formula: modifier = (STR - 10) // 2, attack_bonus = modifier + 2
    
    def test_modifier_average_strength_10(self):
        """Test modifier for STR 10 (average creature)."""
        data = {
            "name": "Average",
            "hit_points": 50,
            "armor_class": [{"value": 12}],
            "strength": 10,
        }
        monster = Monster(data)
        # TODO: STR 10 -> modifier ?, proficiency +2 -> attack bonus ?
        assert monster.attack_bonus == -1  # TODO: Replace -1 with correct value
    
    def test_modifier_strong(self):
        """Test modifier for STR 14 (strong creature)."""
        data = {
            "name": "Strong",
            "hit_points": 50,
            "armor_class": [{"value": 12}],
            "strength": 14,
        }
        monster = Monster(data)
        # TODO: STR 14 -> modifier ?, proficiency +2 -> attack bonus ?
        assert monster.attack_bonus == -1  # TODO: Replace -1 with correct value
    
    def test_modifier_very_strong(self):
        """Test modifier for STR 18 (very strong creature)."""
        data = {
            "name": "Very Strong",
            "hit_points": 50,
            "armor_class": [{"value": 12}],
            "strength": 18,
        }
        monster = Monster(data)
        # TODO: STR 18 -> modifier ?, proficiency +2 -> attack bonus ?
        assert monster.attack_bonus == -1  # TODO: Replace -1 with correct value
    
    def test_modifier_legendary(self):
        """Test modifier for STR 20 (legendary strength)."""
        data = {
            "name": "Legendary",
            "hit_points": 50,
            "armor_class": [{"value": 12}],
            "strength": 20,
        }
        monster = Monster(data)
        # TODO: STR 20 -> modifier ?, proficiency +2 -> attack bonus ?
        assert monster.attack_bonus == -1  # TODO: Replace -1 with correct value
    
    def test_modifier_divine(self):
        """Test modifier for STR 30 (divine/godlike strength)."""
        data = {
            "name": "Divine",
            "hit_points": 500,
            "armor_class": [{"value": 22}],
            "strength": 30,
        }
        monster = Monster(data)
        # TODO: STR 30 -> modifier ?, proficiency +2 -> attack bonus ?
        assert monster.attack_bonus == -1  # TODO: Replace -1 with correct value


class TestStringRepresentations:
    """Test __str__ and __repr__ methods."""
    
    def test_str_returns_name(self):
        """Test that str(monster) returns the monster name."""
        data = {
            "name": "Ancient Dragon",
            "hit_points": 500,
            "armor_class": [{"value": 22}],
            "strength": 27,
        }
        
        monster = Monster(data)
        
        assert str(monster) == "Ancient Dragon"
    
    def test_repr_shows_key_attributes(self):
        """Test that repr(monster) shows name, hp, and ac."""
        data = {
            "name": "Goblin",
            "hit_points": 7,
            "armor_class": [{"value": 15}],
            "strength": 8,
        }
        
        monster = Monster(data)
        
        assert repr(monster) == "Monster(name='Goblin', hp=7, ac=15)"


class TestPropertyCaching:
    """Test that properties return cached values (not recomputed)."""
    
    def test_properties_return_same_values_on_multiple_access(self):
        """Test that accessing properties multiple times returns consistent cached values."""
        data = {
            "name": "Test Monster",
            "hit_points": 100,
            "armor_class": [{"value": 15}],
            "strength": 16,
            "hit_dice": "10d10",
        }
        
        monster = Monster(data)
        
        # Access properties multiple times
        attack1 = monster.attack_bonus
        attack2 = monster.attack_bonus
        damage1 = monster.damage_dice
        damage2 = monster.damage_dice
        parsed1 = monster.damage_dice_parsed
        parsed2 = monster.damage_dice_parsed
        
        # Should return identical values (from cache)
        assert attack1 == attack2 == 5
        assert damage1 == damage2 == "1d10+3"
        assert parsed1 == parsed2 == (1, 10, 3)
        
        # Verify they're the same object (true caching, not recomputation)
        assert parsed1 is parsed2


# ============================================================================
# PHASE 4 TODO: Complete these 2 test functions below
# ============================================================================

# TODO 1: Complete this test for a monster with STR 12
# Expected: STR 12 -> modifier +1, proficiency +2 -> attack bonus +3

def test_modifier_strength_12():
    """Test modifier for STR 12 (slightly strong)."""
    data = {
        "name": "Slightly Strong",
        "hit_points": 50,
        "armor_class": [{"value": 12}],
        "strength": 12,
    }
    monster = Monster(data)
    # TODO: Fill in the correct attack bonus (STR 12 -> modifier +1, prof +2 -> ?)
    assert monster.attack_bonus == -1  # TODO: Replace -1 with correct value


# TODO 2: Complete this test for hit_die_size extraction
# The hit_die_size property should extract the die size from hit_dice notation
# Example: "10d12" -> 12, "5d8" -> 8, "20d20" -> 20

def test_hit_die_size_extraction():
    """Test that hit die size is extracted correctly from hit_dice notation."""
    data = {
        "name": "Large Monster",
        "hit_points": 100,
        "armor_class": [{"value": 15}],
        "strength": 16,
        "hit_dice": "10d12",  # This should extract 12
    }
    monster = Monster(data)
    # TODO: Fill in the correct die size extracted from "10d12"
    assert monster.hit_die_size == -1  # TODO: Replace -1 with correct value

# ============================================================================
# End of TODO section
# ============================================================================
