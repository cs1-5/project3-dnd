"""
Integration tests for Combat System.

These tests verify that:
1. Combat between two monsters runs to completion
2. Winner is correctly determined
3. Statistics are tracked properly
4. Battle logs are generated

Run with: pytest tests/test_integration_combat.py -v
"""

import pytest
from dnd_api import get_monster_details
from combat_system import CombatSystem


@pytest.mark.integration
class TestCombatFlow:
    """Test complete combat flow from start to finish."""
    
    def test_combat_completes_with_winner(self):
        """Test that combat between two monsters completes with a clear winner."""
        # Create two real monsters from API
        goblin = get_monster_details('goblin')
        kobold = get_monster_details('kobold')
        
        # Start combat
        combat = CombatSystem(goblin, kobold)
        
        # Run combat until someone wins
        winner = None
        max_turns = 100  # Safety limit to prevent infinite loops
        
        for turn in range(max_turns):
            # Perform an attack
            combat.perform_attack()
            
            # Check if battle is over
            is_over, winner = combat.is_battle_over()
            
            if is_over:
                break
            
            # Switch to next monster's turn
            combat.switch_turn()
        
        # Verify battle completed
        assert winner is not None, "Combat should complete within 100 turns"
        assert winner in [goblin, kobold], "Winner must be one of the two monsters"
        
        # Verify one monster has 0 HP
        assert combat.monster1_hp == 0 or combat.monster2_hp == 0
        
        # Verify statistics were tracked
        assert combat.monster1_attacks > 0 or combat.monster2_attacks > 0
    
    def test_combat_tracks_statistics(self):
        """Test that combat properly tracks hits, misses, and damage."""
        # Use real monsters
        goblin = get_monster_details('goblin')
        kobold = get_monster_details('kobold')
        
        combat = CombatSystem(goblin, kobold)
        
        # Run combat to completion
        for _ in range(100):
            combat.perform_attack()
            is_over, _ = combat.is_battle_over()
            if is_over:
                break
            combat.switch_turn()
        
        # Get final statistics
        stats = combat.get_battle_statistics()
        
        # Verify both monsters attacked
        assert stats['monster1']['attacks'] > 0
        assert stats['monster2']['attacks'] > 0
        
        # Verify hits were tracked
        assert stats['monster1']['hits'] >= 0
        assert stats['monster2']['hits'] >= 0
        
        # Verify hit rate is between 0 and 1
        assert 0 <= stats['monster1']['actual_hit_rate'] <= 1
        assert 0 <= stats['monster2']['actual_hit_rate'] <= 1
        
        # Verify d20 rolls were tracked
        assert stats['general']['total_rolls'] > 0
        
        # Average d20 roll should be reasonable (between 1 and 20)
        avg_roll = stats['general']['average_roll']
        assert 1 <= avg_roll <= 20
    
    def test_combat_generates_log(self):
        """Test that combat generates a battle log."""
        goblin = get_monster_details('goblin')
        kobold = get_monster_details('kobold')
        
        combat = CombatSystem(goblin, kobold)
        
        # Initially, log should be empty
        assert len(combat.combat_log) == 0
        
        # Perform one attack
        combat.perform_attack()
        
        # Log should have entries now
        assert len(combat.combat_log) > 0
        
        # Log entries should be strings
        assert all(isinstance(entry, str) for entry in combat.combat_log)
    
    def test_critical_hit_detection(self):
        """Test that critical hits (nat 20) are detected and tracked."""
        goblin = get_monster_details('goblin')
        kobold = get_monster_details('kobold')
        
        combat = CombatSystem(goblin, kobold)
        
        # Run many attacks - eventually we'll get a crit (5% chance)
        for _ in range(200):
            combat.perform_attack()
            is_over, _ = combat.is_battle_over()
            if is_over:
                break
            combat.switch_turn()
        
        stats = combat.get_battle_statistics()
        
        # Total crits should be tracked (might be 0 if unlucky, but stat exists)
        total_crits = stats['monster1']['crits'] + stats['monster2']['crits']
        assert total_crits >= 0  # Should be a valid number
        
        # If we got crits, verify they're reasonable
        total_attacks = stats['monster1']['attacks'] + stats['monster2']['attacks']
        if total_attacks > 0:
            crit_rate = total_crits / total_attacks
            # Crit rate should be roughly 5% (but varies with randomness)
            # Just check it's not impossibly high
            assert crit_rate <= 0.20  # Max 20% (very unlucky would be higher than 5%)
    
    def test_monster1_always_goes_first(self):
        """Test that Monster 1 always takes the first turn."""
        goblin = get_monster_details('goblin')
        kobold = get_monster_details('kobold')
        
        combat = CombatSystem(goblin, kobold)
        
        # Current turn should be 1 (Monster 1)
        assert combat.current_turn == 1
        
        # Monster 1 should get the first attack
        combat.perform_attack()
        
        # Monster 1 should have 1 attack recorded
        assert combat.monster1_attacks == 1
        assert combat.monster2_attacks == 0


@pytest.mark.integration
class TestCombatEdgeCases:
    """Test edge cases in combat."""
    
    def test_combat_between_identical_monsters(self):
        """Test combat between two identical monsters (same species)."""
        # Two Goblins fighting each other
        goblin1 = get_monster_details('goblin')
        goblin2 = get_monster_details('goblin')
        
        combat = CombatSystem(goblin1, goblin2)
        
        # Should still complete (one will win due to randomness)
        for _ in range(100):
            combat.perform_attack()
            is_over, winner = combat.is_battle_over()
            if is_over:
                break
            combat.switch_turn()
        
        assert winner is not None
    
    def test_combat_between_very_different_power_levels(self):
        """Test combat between a very weak and very strong monster."""
        # Commoner (weak) vs Orc (strong)
        commoner = get_monster_details('commoner')
        orc = get_monster_details('orc')
        
        combat = CombatSystem(commoner, orc)
        
        # Should complete quickly (orc should dominate)
        for _ in range(50):
            combat.perform_attack()
            is_over, winner = combat.is_battle_over()
            if is_over:
                break
            combat.switch_turn()
        
        # Orc should win (but we won't assert it due to randomness)
        # Just verify someone won
        assert winner is not None

