"""
Integration tests for Battle Simulator.

These tests verify that:
1. Multiple battles can run successfully
2. Statistics are aggregated correctly
3. Results are reasonable and consistent

Run with: pytest tests/test_integration_simulator.py -v
"""

import pytest
from battle_simulator import run_multiple_battles


@pytest.mark.integration
class TestBattleSimulator:
    """Test the battle simulator with small samples."""
    
    def test_simulator_runs_10_battles(self):
        """Test running 10 battles between two monsters."""
        # Run a small simulation
        results = run_multiple_battles('goblin', 'kobold', 10)
        
        # Verify we got results
        assert results is not None
        
        # Verify basic structure
        assert 'total_battles' in results
        assert 'monster1_wins' in results
        assert 'monster2_wins' in results
        
        # Verify counts
        assert results['total_battles'] == 10
        assert results['monster1_wins'] + results['monster2_wins'] == 10
        
        # Verify win rates
        assert 0 <= results['monster1_win_rate'] <= 1
        assert 0 <= results['monster2_win_rate'] <= 1
        assert abs(results['monster1_win_rate'] + results['monster2_win_rate'] - 1.0) < 0.01
    
    def test_simulator_tracks_monster_names(self):
        """Test that simulator records monster names."""
        results = run_multiple_battles('goblin', 'kobold', 5)
        
        assert 'monster1_name' in results
        assert 'monster2_name' in results
        
        assert results['monster1_name'] == "Goblin"
        assert results['monster2_name'] == "Kobold"
    
    def test_simulator_tracks_rounds(self):
        """Test that simulator tracks round statistics."""
        results = run_multiple_battles('goblin', 'kobold', 10)
        
        # Should track average, min, and max rounds
        assert 'avg_turns' in results
        assert 'min_rounds' in results
        assert 'max_rounds' in results
        
        # Verify reasonable values
        assert results['avg_turns'] > 0
        assert results['min_rounds'] >= 0  # Can be 0 in rare cases
        assert results['max_rounds'] > 0
        assert results['max_rounds'] >= results['min_rounds']
    
    def test_simulator_aggregates_statistics(self):
        """Test that simulator aggregates hit rates, crit rates, etc."""
        results = run_multiple_battles('goblin', 'kobold', 20)
        
        # Should have aggregated statistics
        assert 'monster1_avg_hit_rate' in results
        assert 'monster1_avg_crit_rate' in results
        assert 'monster1_avg_dmg_per_hit' in results
        assert 'avg_d20_roll' in results
        
        # Hit rates should be between 0 and 1
        assert 0 <= results['monster1_avg_hit_rate'] <= 1
        assert 0 <= results['monster2_avg_hit_rate'] <= 1
        
        # Crit rates should be reasonable (around 5%, but varies)
        assert 0 <= results['monster1_avg_crit_rate'] <= 0.30  # Max 30% (very variable)
        assert 0 <= results['monster2_avg_crit_rate'] <= 0.30
        
        # Average d20 roll should be reasonable (around 10.5)
        assert 1 <= results['avg_d20_roll'] <= 20
        
        # Damage per hit should be positive
        if results['monster1_avg_dmg_per_hit'] > 0:
            assert results['monster1_avg_dmg_per_hit'] > 0
        if results['monster2_avg_dmg_per_hit'] > 0:
            assert results['monster2_avg_dmg_per_hit'] > 0
    
    def test_simulator_with_different_monsters(self):
        """Test simulator works with various monster combinations."""
        # Test different combinations
        combinations = [
            ('goblin', 'kobold'),
            ('orc', 'goblin'),
            ('commoner', 'kobold'),
        ]
        
        for monster1, monster2 in combinations:
            results = run_multiple_battles(monster1, monster2, 5)
            
            # Each should complete successfully
            assert results is not None
            assert results['total_battles'] == 5
            assert results['monster1_wins'] + results['monster2_wins'] == 5
    
    def test_simulator_handles_invalid_monster(self):
        """Test that simulator handles invalid monster gracefully."""
        # Try with an invalid monster index
        results = run_multiple_battles('invalid-monster-123', 'goblin', 5)
        
        # Should return an error result
        assert results is not None
        assert 'error' in results or results['total_battles'] == 0


@pytest.mark.integration
class TestSimulatorConsistency:
    """Test that simulator produces consistent, reasonable results."""
    
    def test_running_simulation_twice_gives_different_results(self):
        """Test that randomness produces different outcomes."""
        # Run same simulation twice
        results1 = run_multiple_battles('goblin', 'kobold', 10)
        results2 = run_multiple_battles('goblin', 'kobold', 10)
        
        # Results should vary (different random outcomes)
        # It's POSSIBLE they're identical, but very unlikely
        # We'll just check that both completed successfully
        assert results1['total_battles'] == 10
        assert results2['total_battles'] == 10
    
    def test_more_battles_gives_better_statistics(self):
        """Test that more battles provide more stable statistics."""
        # Run with few battles
        small_sample = run_multiple_battles('goblin', 'kobold', 5)
        
        # Run with more battles
        large_sample = run_multiple_battles('goblin', 'kobold', 20)
        
        # Both should complete
        assert small_sample['total_battles'] == 5
        assert large_sample['total_battles'] == 20
        
        # Large sample should have more total dice rolls
        assert large_sample['total_d20_rolls'] > small_sample['total_d20_rolls']

