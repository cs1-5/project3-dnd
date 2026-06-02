"""
Integration tests for student implementations.

These tests verify that all student code works together correctly:
- Phase 1: Dice rolling (randomness)
- Phase 2: Basic probability functions
- Phase 3: Advanced probability (conditional, expected value)
- Full system integration

These tests fail until you complete the implementation tasks, then all should pass.
"""

import pytest
from utils.dice_roller import roll_d20, roll_dice, roll_with_modifier
from probability import (
    calculate_hit_probability,
    calculate_expected_damage,
    calculate_min_roll_needed,
    calculate_damage_range,
    calculate_crit_given_hit,
    calculate_expected_damage_per_attack,
)
from models.monster import Monster
from combat_system import CombatSystem


class TestDiceRollerBasic:
    """Test basic dice rolling functionality (Phase 1)."""
    
    def test_roll_d20_returns_valid_range(self):
        """Test that roll_d20() returns a value between 1 and 20."""
        for _ in range(100):
            roll = roll_d20()
            assert isinstance(roll, int)
            assert 1 <= roll <= 20
    
    def test_roll_dice_returns_correct_length(self):
        """Test that roll_dice returns the correct number of dice."""
        result = roll_dice(3, 6)
        assert isinstance(result, list)
        assert len(result) == 3
        for roll in result:
            assert 1 <= roll <= 6
    
    def test_roll_with_modifier_structure(self):
        """Test that roll_with_modifier returns (total, rolls) tuple."""
        total, rolls = roll_with_modifier(2, 8, 3)
        assert isinstance(total, int)
        assert isinstance(rolls, list)
        assert len(rolls) == 2
        # Total should be sum of rolls + modifier
        assert total == sum(rolls) + 3
    
    def test_roll_with_modifier_minimum_zero(self):
        """Test that damage can't go below 0 even with large negative modifier."""
        total, rolls = roll_with_modifier(1, 4, -10)
        assert total >= 0


class TestDiceRollerStatistical:
    """Test statistical properties of dice rolling (Phase 1)."""
    
    def test_d20_average_close_to_expected(self):
        """Test that rolling d20 many times averages close to 10.5."""
        rolls = [roll_d20() for _ in range(1000)]
        average = sum(rolls) / len(rolls)
        # Expected average of d20 is 10.5
        # With 1000 rolls, should be within 1.0 of expected
        assert 9.5 <= average <= 11.5
    
    def test_d6_average_close_to_expected(self):
        """Test that rolling d6 many times averages close to 3.5."""
        all_rolls = []
        for _ in range(200):
            rolls = roll_dice(1, 6)
            all_rolls.extend(rolls)
        
        average = sum(all_rolls) / len(all_rolls)
        # Expected average of d6 is 3.5
        assert 3.0 <= average <= 4.0
    
    def test_dice_produce_varying_results(self):
        """Test that dice rolls are actually random (not all the same)."""
        rolls = [roll_d20() for _ in range(50)]
        unique_rolls = set(rolls)
        # Should have at least 10 different values in 50 rolls
        assert len(unique_rolls) >= 10


class TestProbabilityCalculations:
    """Test basic probability functions (Phase 2)."""
    
    def test_hit_probability_easy_target(self):
        """Test hit probability for easy-to-hit target."""
        # Attack bonus +10 vs AC 10 -> need 1+ on d20 (but nat 1 always misses)
        prob = calculate_hit_probability(10, 10)
        assert prob == 0.95
    
    def test_hit_probability_moderate(self):
        """Test hit probability for moderate difficulty."""
        # Attack bonus +5 vs AC 15 -> need 10+ on d20
        prob = calculate_hit_probability(5, 15)
        assert prob == 0.55
    
    def test_hit_probability_very_hard(self):
        """Test hit probability for very hard target."""
        # Attack bonus +0 vs AC 20 -> need nat 20
        prob = calculate_hit_probability(0, 20)
        assert prob == 0.05
    
    def test_expected_damage_1d8plus4(self):
        """Test expected damage calculation for 1d8+4."""
        expected = calculate_expected_damage(1, 8, 4)
        # (1+8)/2 + 4 = 4.5 + 4 = 8.5
        assert expected == 8.5
    
    def test_expected_damage_2d6(self):
        """Test expected damage calculation for 2d6."""
        expected = calculate_expected_damage(2, 6, 0)
        # 2 * (1+6)/2 = 2 * 3.5 = 7.0
        assert expected == 7.0
    
    def test_min_roll_needed_moderate(self):
        """Test minimum roll calculation."""
        min_roll = calculate_min_roll_needed(5, 15)
        assert min_roll == 10  # Need 10 on d20
    
    def test_damage_range_1d8plus3(self):
        """Test damage range calculation."""
        min_dmg, max_dmg = calculate_damage_range(1, 8, 3)
        assert min_dmg == 4  # 1 + 3
        assert max_dmg == 11  # 8 + 3


class TestConditionalProbability:
    """Test advanced probability functions (Phase 3)."""
    
    def test_crit_given_hit_moderate_accuracy(self):
        """Test P(crit | hit) for moderate hit rate."""
        # 55% hit rate -> P(crit|hit) = 0.05 / 0.55 ≈ 0.0909
        prob = calculate_crit_given_hit(5, 15)
        assert 0.09 <= prob <= 0.10
    
    def test_crit_given_hit_low_accuracy(self):
        """Test P(crit | hit) for low hit rate."""
        # Attack bonus 0 vs AC 18 -> need 18+ on d20 (18, 19, 20 = 15% hit rate)
        # P(crit|hit) = 0.05 / 0.15 = 0.333...
        prob = calculate_crit_given_hit(0, 18)
        assert 0.32 <= prob <= 0.34
    
    def test_expected_damage_per_attack_accounts_for_misses(self):
        """Test that expected damage per attack includes miss chance."""
        # 55% hit, 8.5 avg damage -> 0.55 * 8.5 = 4.675
        expected = calculate_expected_damage_per_attack(5, 15, 1, 8, 4)
        assert 4.6 <= expected <= 4.8
    
    def test_expected_damage_per_attack_very_low_hit(self):
        """Test expected damage when hit rate is very low."""
        # 5% hit (nat 20 only), 7.0 avg damage -> 0.05 * 7.0 = 0.35
        expected = calculate_expected_damage_per_attack(0, 20, 2, 6, 0)
        assert 0.3 <= expected <= 0.4


class TestFullBattleIntegration:
    """Test that all components work together in a real battle."""
    
    def test_battle_completes_successfully(self):
        """Test that a full battle can run to completion."""
        data1 = {
            "name": "Goblin",
            "hit_points": 7,
            "armor_class": [{"value": 15}],
            "strength": 8,
            "proficiency_bonus": 2,
            "hit_dice": "2d6",
        }
        data2 = {
            "name": "Kobold",
            "hit_points": 5,
            "armor_class": [{"value": 12}],
            "strength": 7,
            "proficiency_bonus": 2,
            "hit_dice": "2d6",
        }
        
        monster1 = Monster(data1)
        monster2 = Monster(data2)
        combat = CombatSystem(monster1, monster2)
        
        # Run battle by performing attacks until someone wins
        max_rounds = 100
        for _ in range(max_rounds):
            combat.perform_attack()
            is_over, winner = combat.is_battle_over()
            if is_over:
                break
        
        # Should be over within 100 rounds
        is_over, winner = combat.is_battle_over()
        assert is_over
        assert winner is not None
        
        # Should have some combat log entries
        assert len(combat.combat_log) > 0
        
        # Should have tracked some attacks
        total_attacks = combat.monster1_attacks + combat.monster2_attacks
        assert total_attacks > 0
    
    def test_battle_tracks_statistics_correctly(self):
        """Test that battle statistics are tracked accurately."""
        data1 = {
            "name": "Strong Monster",
            "hit_points": 30,
            "armor_class": [{"value": 12}],
            "strength": 16,
            "proficiency_bonus": 2,
            "hit_dice": "3d8",
        }
        data2 = {
            "name": "Weak Monster",
            "hit_points": 20,
            "armor_class": [{"value": 10}],
            "strength": 8,
            "proficiency_bonus": 2,
            "hit_dice": "2d6",
        }
        
        monster1 = Monster(data1)
        monster2 = Monster(data2)
        combat = CombatSystem(monster1, monster2)
        
        # Run battle
        max_rounds = 100
        for _ in range(max_rounds):
            combat.perform_attack()
            is_over, winner = combat.is_battle_over()
            if is_over:
                break
        
        # Get statistics
        stats = combat.get_battle_statistics()
        
        # Verify statistics structure (nested in monster1/monster2/general)
        assert 'monster1' in stats
        assert 'monster2' in stats
        assert 'general' in stats
        
        # Verify monster stats
        assert 'attacks' in stats['monster1']
        assert 'hits' in stats['monster1']
        assert 'attacks' in stats['monster2']
        assert 'hits' in stats['monster2']
        
        # Verify logical consistency
        assert stats['monster1']['hits'] <= stats['monster1']['attacks']
        assert stats['monster2']['hits'] <= stats['monster2']['attacks']
        
        # Verify winner is determined
        is_over, winner = combat.is_battle_over()
        assert is_over
        assert winner is not None
    
    def test_probability_calculations_match_monster_stats(self):
        """Test that probability calculations work with real monster data."""
        data = {
            "name": "Test Monster",
            "hit_points": 50,
            "armor_class": [{"value": 15}],
            "strength": 14,  # +2 modifier
            "proficiency_bonus": 3,
            "hit_dice": "5d10",
        }
        
        monster = Monster(data)
        
        # Monster should have correct derived stats
        assert monster.attack_bonus == 5  # +2 (STR) + 3 (prof)
        assert monster.damage_dice == "1d10+2"
        assert monster.damage_dice_parsed == (1, 10, 2)
        
        # Probability calculations should work with monster stats
        hit_prob = calculate_hit_probability(monster.attack_bonus, 12)
        assert 0 < hit_prob < 1
        
        expected_dmg = calculate_expected_damage(1, 10, 2)
        assert expected_dmg == 7.5

