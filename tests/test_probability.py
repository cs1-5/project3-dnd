"""
Unit tests for probability calculation functions.

Run with: pytest tests/test_probability.py
Or: pytest tests/ -v
"""

import pytest
from probability import (
    calculate_hit_probability,
    calculate_expected_damage,
    calculate_crit_probability,
    calculate_damage_range,
    calculate_crit_given_hit,
    calculate_expected_damage_per_attack
)


class TestBasicHit:
    """Test basic hit probability calculations."""
    
    def test_standard_case(self):
        """Test: +5 attack vs AC 15 should be 55%"""
        result = calculate_hit_probability(attack_bonus=5, target_ac=15)
        assert abs(result - 0.55) < 0.001
    
    def test_even_odds(self):
        """Test: +0 attack vs AC 10 should be 55%"""
        result = calculate_hit_probability(attack_bonus=0, target_ac=10)
        assert abs(result - 0.55) < 0.001
    
    def test_difficult_hit(self):
        """Test: +2 attack vs AC 20 should be 15% (need 18+ on d20)"""
        result = calculate_hit_probability(attack_bonus=2, target_ac=20)
        assert abs(result - 0.15) < 0.001
    
    def test_guaranteed_min(self):
        """Test: Very low attack bonus should still have 5% (nat 20)"""
        result = calculate_hit_probability(attack_bonus=-5, target_ac=25)
        assert abs(result - 0.05) < 0.001
    
    def test_auto_hit_max(self):
        """Test: Very high attack should be 95% (nat 1 auto-miss)"""
        result = calculate_hit_probability(attack_bonus=20, target_ac=10)
        assert abs(result - 0.95) < 0.001


class TestExpectedDamage:
    """Test expected damage calculations."""
    
    def test_1d8_plus_3(self):
        """Test: 1d8+3 should average 7.5"""
        result = calculate_expected_damage(1, 8, 3)
        assert abs(result - 7.5) < 0.001
    
    def test_2d6(self):
        """Test: 2d6 should average 7.0"""
        result = calculate_expected_damage(2, 6, 0)
        assert abs(result - 7.0) < 0.001
    
    def test_1d4_minus_1(self):
        """Test: 1d4-1 should average 1.5"""
        result = calculate_expected_damage(1, 4, -1)
        assert abs(result - 1.5) < 0.001
    
    def test_3d6_plus_4(self):
        """Test: 3d6+4 should average 14.5"""
        result = calculate_expected_damage(3, 6, 4)
        assert abs(result - 14.5) < 0.001


class TestCriticalHit:
    """Test critical hit probability."""
    
    def test_always_5_percent(self):
        """Test: Crit probability is always 5% (1/20)"""
        result = calculate_crit_probability()
        assert abs(result - 0.05) < 0.001


class TestDamageRange:
    """Test damage range calculations."""
    
    def test_1d8_plus_3(self):
        """Test: 1d8+3 should be 4-11"""
        min_dmg, max_dmg = calculate_damage_range(1, 8, 3)
        assert min_dmg == 4
        assert max_dmg == 11
    
    def test_2d6(self):
        """Test: 2d6 should be 2-12"""
        min_dmg, max_dmg = calculate_damage_range(2, 6, 0)
        assert min_dmg == 2
        assert max_dmg == 12
    
    def test_1d4_minus_1(self):
        """Test: 1d4-1 should be 0-3 (minimum damage is 0)"""
        min_dmg, max_dmg = calculate_damage_range(1, 4, -1)
        assert min_dmg == 0  # Cannot go below 0
        assert max_dmg == 3


class TestConditionalProbability:
    """Test conditional probability: P(crit | hit)."""
    
    def test_crit_given_hit_easy_target(self):
        """Test: Easy target (95% hit) → P(crit|hit) ≈ 5.26%"""
        # +10 attack vs AC 10 → 95% hit rate
        result = calculate_crit_given_hit(attack_bonus=10, target_ac=10)
        expected = 0.05 / 0.95  # P(crit) / P(hit) ≈ 0.0526
        assert abs(result - expected) < 0.001
    
    def test_crit_given_hit_moderate_target(self):
        """Test: Moderate target (55% hit) → P(crit|hit) ≈ 9.09%"""
        # +5 attack vs AC 15 → 55% hit rate
        result = calculate_crit_given_hit(attack_bonus=5, target_ac=15)
        expected = 0.05 / 0.55  # ≈ 0.0909
        assert abs(result - expected) < 0.001
    
    def test_crit_given_hit_hard_target(self):
        """Test: Hard target (25% hit) → P(crit|hit) = 20%!"""
        # +0 attack vs AC 16 → 25% hit rate (need 16+)
        result = calculate_crit_given_hit(attack_bonus=0, target_ac=16)
        expected = 0.05 / 0.25  # = 0.20 (20%!)
        assert abs(result - expected) < 0.001
    
    def test_crit_given_hit_very_hard_target(self):
        """Test: Very hard target (5% hit, nat 20 only) → P(crit|hit) = 100%!"""
        # +0 attack vs AC 20 → Only natural 20 hits
        result = calculate_crit_given_hit(attack_bonus=0, target_ac=20)
        expected = 1.0  # Every hit MUST be a crit!
        assert abs(result - expected) < 0.001


class TestExpectedDamagePerAttack:
    """Test expected damage accounting for miss chance."""
    
    def test_expected_damage_per_attack_guaranteed_hit(self):
        """Test: Auto-hit (95%) → almost full damage"""
        # +10 attack vs AC 10, 1d8+3 (avg 7.5)
        result = calculate_expected_damage_per_attack(10, 10, 1, 8, 3)
        expected = 0.95 * 7.5  # 7.125
        assert abs(result - expected) < 0.001
    
    def test_expected_damage_per_attack_moderate_hit(self):
        """Test: 55% hit rate → reduced expected damage"""
        # +5 attack vs AC 15, 1d8+3 (avg 7.5)
        result = calculate_expected_damage_per_attack(5, 15, 1, 8, 3)
        expected = 0.55 * 7.5  # 4.125
        assert abs(result - expected) < 0.001
    
    def test_expected_damage_per_attack_hard_hit(self):
        """Test: 25% hit rate → much lower expected damage"""
        # +0 attack vs AC 16, 2d6 (avg 7.0)
        result = calculate_expected_damage_per_attack(0, 16, 2, 6, 0)
        expected = 0.25 * 7.0  # 1.75
        assert abs(result - expected) < 0.001
    
    def test_expected_damage_per_attack_nat_20_only(self):
        """Test: Only nat 20 hits (5%) → very low expected damage"""
        # +0 attack vs AC 20, 2d6 (avg 7.0)
        result = calculate_expected_damage_per_attack(0, 20, 2, 6, 0)
        expected = 0.05 * 7.0  # 0.35
        assert abs(result - expected) < 0.001


# STUDENT EXERCISES: Add tests for your formulas below!


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])

