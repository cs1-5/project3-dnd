"""
Battle Simulator for running multiple battles automatically.
Used for demonstrating the Law of Large Numbers and probability convergence.
"""

from typing import Dict, Callable, Optional
from dnd_api import get_monster_details
from combat_system import CombatSystem


def run_multiple_battles(monster1_index: str, monster2_index: str, num_battles: int) -> Dict:
    """
    Run multiple battles between two monsters and return aggregated statistics.
    
    Args:
        monster1_index: Index of the first monster in the API
        monster2_index: Index of the second monster in the API
        num_battles: Number of battles to simulate
    
    Returns:
        Dictionary with aggregated results:
        - monster1_wins: Number of times monster 1 won
        - monster2_wins: Number of times monster 2 won
        - avg_turns: Average number of turns per battle
        - total_battles: Total battles run
        - monster1_win_rate: Win rate as decimal (0.0 to 1.0)
        - monster2_win_rate: Win rate as decimal (0.0 to 1.0)
    """
    # Fetch monster details once
    monster1 = get_monster_details(monster1_index)
    monster2 = get_monster_details(monster2_index)
    
    if not monster1 or not monster2:
        return {
            'error': 'Failed to load monster details',
            'monster1_wins': 0,
            'monster2_wins': 0,
            'total_battles': 0,
        }
    
    monster1_wins = 0
    monster2_wins = 0
    total_turns = 0
    min_rounds = float('inf')
    max_rounds = 0
    
    # Track aggregated statistics for Law of Large Numbers
    total_m1_attacks = 0
    total_m1_hits = 0
    total_m1_crits = 0
    total_m1_damage = 0  # Total damage dealt (for avg per hit)
    total_m2_attacks = 0
    total_m2_hits = 0
    total_m2_crits = 0
    total_m2_damage = 0
    all_d20_rolls = []
    
    # Run all battles
    for _ in range(num_battles):
        combat = CombatSystem(monster1, monster2)
        
        # Run battle until completion (max 1000 turns to prevent infinite loops)
        max_turns = 1000
        turn_count = 0
        
        while turn_count < max_turns:
            combat.perform_attack()
            is_over, winner = combat.is_battle_over()
            
            if is_over:
                if winner == monster1:
                    monster1_wins += 1
                else:
                    monster2_wins += 1
                total_turns += combat.turn_count
                min_rounds = min(min_rounds, combat.turn_count)
                max_rounds = max(max_rounds, combat.turn_count)
                
                # Aggregate statistics from this battle
                total_m1_attacks += combat.monster1_attacks
                total_m1_hits += combat.monster1_hits
                total_m1_crits += combat.monster1_crits
                total_m1_damage += combat.monster1_total_damage
                total_m2_attacks += combat.monster2_attacks
                total_m2_hits += combat.monster2_hits
                total_m2_crits += combat.monster2_crits
                total_m2_damage += combat.monster2_total_damage
                all_d20_rolls.extend(combat.all_rolls)
                break
            
            combat.switch_turn()
            turn_count += 1
    
    avg_turns = total_turns / num_battles if num_battles > 0 else 0
    
    # Calculate aggregated statistics
    m1_avg_hit_rate = total_m1_hits / total_m1_attacks if total_m1_attacks > 0 else 0
    m1_avg_crit_rate = total_m1_crits / total_m1_attacks if total_m1_attacks > 0 else 0
    m1_avg_dmg_per_hit = total_m1_damage / total_m1_hits if total_m1_hits > 0 else 0
    
    m2_avg_hit_rate = total_m2_hits / total_m2_attacks if total_m2_attacks > 0 else 0
    m2_avg_crit_rate = total_m2_crits / total_m2_attacks if total_m2_attacks > 0 else 0
    m2_avg_dmg_per_hit = total_m2_damage / total_m2_hits if total_m2_hits > 0 else 0
    
    avg_d20_roll = sum(all_d20_rolls) / len(all_d20_rolls) if all_d20_rolls else 0
    
    return {
        'monster1_wins': monster1_wins,
        'monster2_wins': monster2_wins,
        'total_battles': num_battles,
        'monster1_win_rate': monster1_wins / num_battles if num_battles > 0 else 0,
        'monster2_win_rate': monster2_wins / num_battles if num_battles > 0 else 0,
        'avg_turns': avg_turns,
        'min_rounds': min_rounds if min_rounds != float('inf') else 0,
        'max_rounds': max_rounds,
        'monster1_name': monster1.name,
        'monster2_name': monster2.name,
        # Aggregated statistics for Law of Large Numbers
        'monster1_avg_hit_rate': m1_avg_hit_rate,
        'monster1_avg_crit_rate': m1_avg_crit_rate,
        'monster1_avg_dmg_per_hit': m1_avg_dmg_per_hit,
        'monster2_avg_hit_rate': m2_avg_hit_rate,
        'monster2_avg_crit_rate': m2_avg_crit_rate,
        'monster2_avg_dmg_per_hit': m2_avg_dmg_per_hit,
        'avg_d20_roll': avg_d20_roll,
        'total_d20_rolls': len(all_d20_rolls),
    }


def run_multiple_battles_with_callback(
    monster1_index: str, 
    monster2_index: str, 
    num_battles: int,
    update_callback: Optional[Callable[[Dict], None]] = None,
    update_frequency: int = 10
) -> Dict:
    """
    Run multiple battles with live progress updates via callback.
    
    Args:
        monster1_index: Index of the first monster in the API
        monster2_index: Index of the second monster in the API
        num_battles: Number of battles to simulate
        update_callback: Optional function called periodically with current results
        update_frequency: How often to call the callback (every N battles)
    
    Returns:
        Dictionary with final aggregated results (same as run_multiple_battles)
    """
    # Fetch monster details once
    monster1 = get_monster_details(monster1_index)
    monster2 = get_monster_details(monster2_index)
    
    if not monster1 or not monster2:
        return {
            'error': 'Failed to load monster details',
            'monster1_wins': 0,
            'monster2_wins': 0,
            'total_battles': 0,
        }
    
    monster1_wins = 0
    monster2_wins = 0
    total_turns = 0
    min_rounds = float('inf')
    max_rounds = 0
    win_rate_history = []  # Track win rate over time for convergence visualization
    
    # Track aggregated statistics for Law of Large Numbers
    total_m1_attacks = 0
    total_m1_hits = 0
    total_m1_crits = 0
    total_m1_damage = 0  # Total damage dealt (for avg per hit)
    total_m2_attacks = 0
    total_m2_hits = 0
    total_m2_crits = 0
    total_m2_damage = 0
    all_d20_rolls = []
    
    # Adjust update frequency for smooth updates
    actual_update_freq = max(1, min(update_frequency, num_battles // 20))
    
    # Run all battles
    for battle_num in range(1, num_battles + 1):
        combat = CombatSystem(monster1, monster2)
        
        # Run battle until completion (max 1000 turns to prevent infinite loops)
        max_turns = 1000
        turn_count = 0
        
        while turn_count < max_turns:
            combat.perform_attack()
            is_over, winner = combat.is_battle_over()
            
            if is_over:
                if winner == monster1:
                    monster1_wins += 1
                else:
                    monster2_wins += 1
                total_turns += combat.turn_count
                min_rounds = min(min_rounds, combat.turn_count)
                max_rounds = max(max_rounds, combat.turn_count)
                
                # Aggregate statistics from this battle
                total_m1_attacks += combat.monster1_attacks
                total_m1_hits += combat.monster1_hits
                total_m1_crits += combat.monster1_crits
                total_m1_damage += combat.monster1_total_damage
                total_m2_attacks += combat.monster2_attacks
                total_m2_hits += combat.monster2_hits
                total_m2_crits += combat.monster2_crits
                total_m2_damage += combat.monster2_total_damage
                all_d20_rolls.extend(combat.all_rolls)
                break
            
            combat.switch_turn()
            turn_count += 1
        
        # Call update callback at specified frequency
        if update_callback and (battle_num % actual_update_freq == 0 or battle_num == num_battles):
            current_win_rate = monster1_wins / battle_num
            win_rate_history.append((battle_num, current_win_rate))
            
            # Calculate current aggregated statistics
            curr_m1_avg_hit_rate = total_m1_hits / total_m1_attacks if total_m1_attacks > 0 else 0
            curr_m1_avg_crit_rate = total_m1_crits / total_m1_attacks if total_m1_attacks > 0 else 0
            curr_m1_avg_dmg_per_hit = total_m1_damage / total_m1_hits if total_m1_hits > 0 else 0
            curr_m2_avg_hit_rate = total_m2_hits / total_m2_attacks if total_m2_attacks > 0 else 0
            curr_m2_avg_crit_rate = total_m2_crits / total_m2_attacks if total_m2_attacks > 0 else 0
            curr_m2_avg_dmg_per_hit = total_m2_damage / total_m2_hits if total_m2_hits > 0 else 0
            curr_avg_d20_roll = sum(all_d20_rolls) / len(all_d20_rolls) if all_d20_rolls else 0
            
            current_results = {
                'completed': battle_num,
                'total': num_battles,
                'monster1_wins': monster1_wins,
                'monster2_wins': monster2_wins,
                'monster1_win_rate': current_win_rate,
                'monster2_win_rate': (battle_num - monster1_wins) / battle_num,
                'avg_turns': total_turns / battle_num,
                'min_rounds': min_rounds if min_rounds != float('inf') else 0,
                'max_rounds': max_rounds,
                'monster1_name': monster1.name,
                'monster2_name': monster2.name,
                'win_rate_history': win_rate_history.copy(),
                # Include aggregated statistics
                'monster1_avg_hit_rate': curr_m1_avg_hit_rate,
                'monster1_avg_crit_rate': curr_m1_avg_crit_rate,
                'monster1_avg_dmg_per_hit': curr_m1_avg_dmg_per_hit,
                'monster2_avg_hit_rate': curr_m2_avg_hit_rate,
                'monster2_avg_crit_rate': curr_m2_avg_crit_rate,
                'monster2_avg_dmg_per_hit': curr_m2_avg_dmg_per_hit,
                'avg_d20_roll': curr_avg_d20_roll,
                'total_d20_rolls': len(all_d20_rolls),
            }
            update_callback(current_results)
    
    avg_turns = total_turns / num_battles if num_battles > 0 else 0
    
    # Calculate final aggregated statistics
    m1_avg_hit_rate = total_m1_hits / total_m1_attacks if total_m1_attacks > 0 else 0
    m1_avg_crit_rate = total_m1_crits / total_m1_attacks if total_m1_attacks > 0 else 0
    m1_avg_dmg_per_hit = total_m1_damage / total_m1_hits if total_m1_hits > 0 else 0
    
    m2_avg_hit_rate = total_m2_hits / total_m2_attacks if total_m2_attacks > 0 else 0
    m2_avg_crit_rate = total_m2_crits / total_m2_attacks if total_m2_attacks > 0 else 0
    m2_avg_dmg_per_hit = total_m2_damage / total_m2_hits if total_m2_hits > 0 else 0
    
    avg_d20_roll = sum(all_d20_rolls) / len(all_d20_rolls) if all_d20_rolls else 0
    
    return {
        'monster1_wins': monster1_wins,
        'monster2_wins': monster2_wins,
        'total_battles': num_battles,
        'monster1_win_rate': monster1_wins / num_battles if num_battles > 0 else 0,
        'monster2_win_rate': monster2_wins / num_battles if num_battles > 0 else 0,
        'avg_turns': avg_turns,
        'min_rounds': min_rounds if min_rounds != float('inf') else 0,
        'max_rounds': max_rounds,
        'monster1_name': monster1.name,
        'monster2_name': monster2.name,
        'win_rate_history': win_rate_history,
        # Aggregated statistics for Law of Large Numbers
        'monster1_avg_hit_rate': m1_avg_hit_rate,
        'monster1_avg_crit_rate': m1_avg_crit_rate,
        'monster1_avg_dmg_per_hit': m1_avg_dmg_per_hit,
        'monster2_avg_hit_rate': m2_avg_hit_rate,
        'monster2_avg_crit_rate': m2_avg_crit_rate,
        'monster2_avg_dmg_per_hit': m2_avg_dmg_per_hit,
        'avg_d20_roll': avg_d20_roll,
        'total_d20_rolls': len(all_d20_rolls),
    }

