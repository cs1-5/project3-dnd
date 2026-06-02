from typing import Tuple, Optional, Dict
from models.monster import Monster
from probability import (
    calculate_hit_probability,
    calculate_expected_damage,
    calculate_crit_probability
)
from utils.dice_roller import roll_d20, roll_with_modifier


class CombatSystem:
    """Handles simplified combat mechanics with probability-based attacks.
    
    Combat is turn-based with Monster 1 always starting first.
    Attacks use d20 + Attack Bonus vs Defense (AC).
    Natural 20 = Critical Hit (double damage dice), Natural 1 = Critical Miss.
    """
    
    def __init__(self, monster1: Monster, monster2: Monster):
        self.monster1 = monster1
        self.monster2 = monster2
        self.monster1_hp = monster1.hp
        self.monster2_hp = monster2.hp
        self.current_turn = 1  # Monster 1 always goes first
        self.combat_log = []
        
        # Statistics tracking
        self.monster1_attacks = 0
        self.monster2_attacks = 0
        self.monster1_hits = 0
        self.monster2_hits = 0
        self.monster1_crits = 0
        self.monster2_crits = 0
        self.monster1_total_damage = 0
        self.monster2_total_damage = 0
        self.all_rolls = []  # Track all d20 rolls
        self.turn_count = 0
    
    def get_current_attacker(self) -> Monster:
        """Get the monster whose turn it is."""
        return self.monster1 if self.current_turn == 1 else self.monster2
    
    def get_current_defender(self) -> Monster:
        """Get the monster being attacked."""
        return self.monster2 if self.current_turn == 1 else self.monster1
    
    def perform_attack(self) -> Tuple[bool, int, str, int, list, str]:
        """
        Perform an attack from current attacker to defender.
        
        Returns:
            Tuple of (hit: bool, damage: int, message: str, attack_roll: int, damage_rolls: list, damage_dice_str: str)
        """
        attacker = self.get_current_attacker()
        defender = self.get_current_defender()
        
        # Track attack attempt
        if self.current_turn == 1:
            self.monster1_attacks += 1
        else:
            self.monster2_attacks += 1
        
        # Roll to hit (d20 + attack bonus)
        attack_roll = roll_d20()
        self.all_rolls.append(attack_roll)  # Track roll
        attack_bonus = attacker.attack_bonus
        total_attack = attack_roll + attack_bonus
        
        # Check if hit (unless natural 1 or 20)
        hit = total_attack >= defender.ac
        
        if attack_roll == 20:
            # Critical hit!
            num_dice, die_size, modifier = attacker.damage_dice_parsed
            damage, damage_rolls = roll_with_modifier(num_dice * 2, die_size, modifier)  # Double damage dice
            message = f"🎯 CRITICAL HIT! {attacker.name} rolls {attack_roll}+{attack_bonus}={total_attack} vs Defense (AC) {defender.ac}"
            self.combat_log.append(message)
            self.combat_log.append(f"💥 Deals {damage} damage!")
            
            # Track statistics
            if self.current_turn == 1:
                self.monster1_hits += 1
                self.monster1_crits += 1
                self.monster1_total_damage += damage
                self.monster2_hp = max(0, self.monster2_hp - damage)
            else:
                self.monster2_hits += 1
                self.monster2_crits += 1
                self.monster2_total_damage += damage
                self.monster1_hp = max(0, self.monster1_hp - damage)
            
            return True, damage, message, attack_roll, damage_rolls, attacker.damage_dice
        
        elif attack_roll == 1:
            # Critical miss!
            message = f"💨 CRITICAL MISS! {attacker.name} rolls a 1!"
            self.combat_log.append(message)
            return False, 0, message, attack_roll, [], ""
        
        elif hit:
            # Normal hit
            num_dice, die_size, modifier = attacker.damage_dice_parsed
            damage, damage_rolls = roll_with_modifier(num_dice, die_size, modifier)
            message = f"⚔️ {attacker.name} hits! Rolled {attack_roll}+{attack_bonus}={total_attack} vs Defense (AC) {defender.ac}"
            self.combat_log.append(message)
            self.combat_log.append(f"💥 Deals {damage} damage!")
            
            # Track statistics
            if self.current_turn == 1:
                self.monster1_hits += 1
                self.monster1_total_damage += damage
                self.monster2_hp = max(0, self.monster2_hp - damage)
            else:
                self.monster2_hits += 1
                self.monster2_total_damage += damage
                self.monster1_hp = max(0, self.monster1_hp - damage)
            
            return True, damage, message, attack_roll, damage_rolls, attacker.damage_dice
        
        else:
            # Miss
            message = f"❌ {attacker.name} misses! Rolled {attack_roll}+{attack_bonus}={total_attack} vs Defense (AC) {defender.ac}"
            self.combat_log.append(message)
            return False, 0, message, attack_roll, [], ""
    
    def switch_turn(self):
        """Switch to the other monster's turn."""
        self.current_turn = 2 if self.current_turn == 1 else 1
        self.turn_count += 1
        # Add turn divider to combat log
        self.combat_log.append(f"━━━ Turn {self.turn_count} ━━━")
        
    def is_battle_over(self) -> Tuple[bool, Optional[Monster]]:
        """
        Check if battle is over.
        
        Returns:
            Tuple of (is_over: bool, winner: Optional[Monster])
        """
        if self.monster1_hp <= 0:
            return True, self.monster2
        elif self.monster2_hp <= 0:
            return True, self.monster1
        return False, None
    
    def get_battle_statistics(self) -> Dict:
        """
        Get battle statistics comparing actual vs theoretical outcomes.
        
        Returns:
            Dictionary with battle statistics
        """
        # Calculate theoretical values
        m1_attack_bonus = self.monster1.attack_bonus
        m2_attack_bonus = self.monster2.attack_bonus
        
        m1_hit_prob = calculate_hit_probability(m1_attack_bonus, self.monster2.ac)
        m2_hit_prob = calculate_hit_probability(m2_attack_bonus, self.monster1.ac)
        
        num_dice_1, die_size_1, mod_1 = self.monster1.damage_dice_parsed
        num_dice_2, die_size_2, mod_2 = self.monster2.damage_dice_parsed
        m1_expected_dmg = calculate_expected_damage(num_dice_1, die_size_1, mod_1)
        m2_expected_dmg = calculate_expected_damage(num_dice_2, die_size_2, mod_2)
        
        crit_prob = calculate_crit_probability()
        
        # Calculate actual rates
        m1_actual_hit_rate = (self.monster1_hits / self.monster1_attacks) if self.monster1_attacks > 0 else 0
        m2_actual_hit_rate = (self.monster2_hits / self.monster2_attacks) if self.monster2_attacks > 0 else 0
        
        m1_actual_crit_rate = (self.monster1_crits / self.monster1_attacks) if self.monster1_attacks > 0 else 0
        m2_actual_crit_rate = (self.monster2_crits / self.monster2_attacks) if self.monster2_attacks > 0 else 0
        
        m1_actual_avg_dmg = (self.monster1_total_damage / self.monster1_hits) if self.monster1_hits > 0 else 0
        m2_actual_avg_dmg = (self.monster2_total_damage / self.monster2_hits) if self.monster2_hits > 0 else 0
        
        avg_roll = sum(self.all_rolls) / len(self.all_rolls) if self.all_rolls else 0
        
        return {
            'monster1': {
                'attacks': self.monster1_attacks,
                'hits': self.monster1_hits,
                'crits': self.monster1_crits,
                'actual_hit_rate': m1_actual_hit_rate,
                'expected_hit_rate': m1_hit_prob,
                'actual_crit_rate': m1_actual_crit_rate,
                'expected_crit_rate': crit_prob,
                'actual_avg_damage': m1_actual_avg_dmg,
                'expected_avg_damage': m1_expected_dmg,
            },
            'monster2': {
                'attacks': self.monster2_attacks,
                'hits': self.monster2_hits,
                'crits': self.monster2_crits,
                'actual_hit_rate': m2_actual_hit_rate,
                'expected_hit_rate': m2_hit_prob,
                'actual_crit_rate': m2_actual_crit_rate,
                'expected_crit_rate': crit_prob,
                'actual_avg_damage': m2_actual_avg_dmg,
                'expected_avg_damage': m2_expected_dmg,
            },
            'general': {
                'total_turns': self.turn_count,
                'total_rolls': len(self.all_rolls),
                'average_roll': avg_roll,
                'expected_average_roll': 10.5,
            }
        }

