import flet as ft
from dnd_api import get_monster_details
from models.monster import Monster
from combat_system import CombatSystem
from probability import (
    calculate_hit_probability,
    calculate_expected_damage,
    calculate_min_roll_needed,
    calculate_damage_range,
    calculate_crit_probability,
    calculate_crit_given_hit,
    calculate_expected_damage_per_attack
)
from ui_constants import (
    SPACING_XS, SPACING_SM,
    BUTTON_HEIGHT_SM, BUTTON_WIDTH_SM, BUTTON_WIDTH_MD,
    COMBAT_LOG_HEIGHT, HP_BAR_WIDTH,
    TEXT_SIZE_SM, TEXT_SIZE_MD, TEXT_SIZE_LG, TEXT_SIZE_XL
)
from ui_utils import get_probability_color, format_percentage, format_percentage_precise


def battle_screen(page: ft.Page, monster1_index: str, monster2_index: str, on_back):
    """Render the battle screen with combat functionality and probability displays.
    
    Args:
        page: The Flet page object
        monster1_index: Index of the first monster
        monster2_index: Index of the second monster
        on_back: Callback function to go back to monster selection
    """
    # Fetch monster details
    monster1 = get_monster_details(monster1_index)
    monster2 = get_monster_details(monster2_index)
    
    if not monster1 or not monster2:
        page.snack_bar = ft.SnackBar(ft.Text("Error loading monster details!"))
        page.snack_bar.open = True
        page.update()
        return ft.Text("Error loading monsters", color=ft.Colors.RED)
    
    # Initialize combat system
    combat = CombatSystem(monster1, monster2)
    
    # UI Components
    monster1_hp_bar = ft.ProgressBar(
        value=1.0,
        bar_height=10,
        color=ft.Colors.GREEN,
        bgcolor=ft.Colors.RED_900,
        width=HP_BAR_WIDTH,
    )
    
    monster1_hp_text = ft.Text(
        f"HP: {combat.monster1_hp}/{monster1.hp}",
        size=TEXT_SIZE_MD,
        color=ft.Colors.WHITE,
    )
    
    monster2_hp_bar = ft.ProgressBar(
        value=1.0,
        bar_height=10,
        color=ft.Colors.GREEN,
        bgcolor=ft.Colors.RED_900,
        width=HP_BAR_WIDTH,
    )
    
    monster2_hp_text = ft.Text(
        f"HP: {combat.monster2_hp}/{monster2.hp}",
        size=TEXT_SIZE_MD,
        color=ft.Colors.WHITE,
    )
    
    # Last roll displays for each monster
    monster1_last_roll = ft.Text(
        "",
        size=TEXT_SIZE_SM,
        color=ft.Colors.GREY_500,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )
    
    monster2_last_roll = ft.Text(
        "",
        size=TEXT_SIZE_SM,
        color=ft.Colors.GREY_500,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )
    
    turn_indicator = ft.Text(
        f"{combat.get_current_attacker().name}'s Turn",
        size=TEXT_SIZE_LG,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.YELLOW,
        text_align=ft.TextAlign.CENTER,
    )
    
    # Probability info panels - one for each monster
    # Monster 1's attack probabilities (Amber theme)
    m1_prob_hit_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.AMBER_300)
    m1_prob_roll_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.AMBER_200)
    m1_prob_damage_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.AMBER_200)
    m1_prob_crit_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.AMBER_200)
    m1_prob_crit_given_hit_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.AMBER_200)
    m1_prob_expected_dmg_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.AMBER_200)
    
    # Monster 2's attack probabilities (Blue theme)
    m2_prob_hit_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.BLUE_300)
    m2_prob_roll_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.BLUE_200)
    m2_prob_damage_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.BLUE_200)
    m2_prob_crit_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.BLUE_200)
    m2_prob_crit_given_hit_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.BLUE_200)
    m2_prob_expected_dmg_text = ft.Text("", size=TEXT_SIZE_SM, color=ft.Colors.BLUE_200)
    
    # Probability containers for each monster (initially both hidden)
    m1_prob_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("⚔️ Attack Probabilities", size=TEXT_SIZE_MD, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_300),
                ft.Container(height=SPACING_XS),
                m1_prob_hit_text,
                m1_prob_roll_text,
                m1_prob_damage_text,
                m1_prob_expected_dmg_text,
                ft.Container(height=SPACING_XS),
                m1_prob_crit_text,
                m1_prob_crit_given_hit_text,
            ],
            spacing=2,
        ),
        bgcolor=ft.Colors.BLACK38,
        border=ft.border.all(2, ft.Colors.AMBER_700),
        border_radius=5,
        padding=10,
        visible=False,
    )
    
    m2_prob_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("⚔️ Attack Probabilities", size=TEXT_SIZE_MD, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300),
                ft.Container(height=SPACING_XS),
                m2_prob_hit_text,
                m2_prob_roll_text,
                m2_prob_damage_text,
                m2_prob_expected_dmg_text,
                ft.Container(height=SPACING_XS),
                m2_prob_crit_text,
                m2_prob_crit_given_hit_text,
            ],
            spacing=2,
        ),
        bgcolor=ft.Colors.BLACK38,
        border=ft.border.all(2, ft.Colors.BLUE_700),
        border_radius=5,
        padding=10,
        visible=False,
    )
    
    
    combat_log_column = ft.Column(
        [ft.Text(log, size=TEXT_SIZE_SM, color=ft.Colors.GREY_300) for log in combat.combat_log],
        spacing=SPACING_XS,
        scroll=ft.ScrollMode.AUTO,
        height=COMBAT_LOG_HEIGHT,
    )
    
    attack_button = ft.ElevatedButton(
        "⚔️ ATTACK",
        width=BUTTON_WIDTH_MD,
        height=BUTTON_HEIGHT_SM,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.RED_700,
            color=ft.Colors.WHITE,
        ),
    )
    
    monte_carlo_button = ft.ElevatedButton(
        "📊 Monte Carlo",
        width=BUTTON_WIDTH_SM,
        height=BUTTON_HEIGHT_SM,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.DEEP_PURPLE_700,
            color=ft.Colors.WHITE,
        ),
    )
    
    stats_container = ft.Container(visible=False)
    
    def update_probability_display():
        """Update the probability information panel for the active attacker."""
        attacker = combat.get_current_attacker()
        defender = combat.get_current_defender()
        
        attack_bonus = attacker.attack_bonus
        num_dice, die_size, modifier = attacker.damage_dice_parsed
        hit_prob = calculate_hit_probability(attack_bonus, defender.ac)
        min_roll = calculate_min_roll_needed(attack_bonus, defender.ac)
        expected_dmg = calculate_expected_damage(num_dice, die_size, modifier)
        dmg_min, dmg_max = calculate_damage_range(num_dice, die_size, modifier)
        crit_prob = calculate_crit_probability()
        
        # NEW: Conditional probability calculations
        crit_given_hit = calculate_crit_given_hit(attack_bonus, defender.ac)
        expected_dmg_per_attack = calculate_expected_damage_per_attack(
            attack_bonus, defender.ac, num_dice, die_size, modifier
        )
        
        # Determine which monster is attacking (1 or 2)
        is_monster1_turn = (combat.current_turn == 1)
        
        # Update the appropriate monster's probability texts
        if is_monster1_turn:
            m1_prob_hit_text.value = f"Hit: {format_percentage_precise(hit_prob)}"
            m1_prob_hit_text.color = get_probability_color(hit_prob)
            m1_prob_roll_text.value = f"Need {min_roll}+ on d20 (Defense {defender.ac})"
            m1_prob_damage_text.value = f"{attacker.damage_dice} → {dmg_min}-{dmg_max} (avg {expected_dmg:.1f})"
            m1_prob_expected_dmg_text.value = f"Expected per attack: {expected_dmg_per_attack:.2f}"
            m1_prob_crit_text.value = f"Crit: {format_percentage(crit_prob)}"
            m1_prob_crit_given_hit_text.value = f"Crit | Hit: {format_percentage_precise(crit_given_hit)}"
            
            # Show monster 1's probabilities, hide monster 2's
            m1_prob_container.visible = True
            m2_prob_container.visible = False
        else:
            m2_prob_hit_text.value = f"Hit: {format_percentage_precise(hit_prob)}"
            m2_prob_hit_text.color = get_probability_color(hit_prob)
            m2_prob_roll_text.value = f"Need {min_roll}+ on d20 (Defense {defender.ac})"
            m2_prob_damage_text.value = f"{attacker.damage_dice} → {dmg_min}-{dmg_max} (avg {expected_dmg:.1f})"
            m2_prob_expected_dmg_text.value = f"Expected per attack: {expected_dmg_per_attack:.2f}"
            m2_prob_crit_text.value = f"Crit: {format_percentage(crit_prob)}"
            m2_prob_crit_given_hit_text.value = f"Crit | Hit: {format_percentage_precise(crit_given_hit)}"
            
            # Show monster 2's probabilities, hide monster 1's
            m1_prob_container.visible = False
            m2_prob_container.visible = True
    
    def update_ui():
        """Update all UI components with current combat state."""
        # Update HP bars
        monster1_hp_bar.value = max(0, combat.monster1_hp / monster1.hp)
        monster1_hp_text.value = f"HP: {combat.monster1_hp}/{monster1.hp}"
        
        monster2_hp_bar.value = max(0, combat.monster2_hp / monster2.hp)
        monster2_hp_text.value = f"HP: {combat.monster2_hp}/{monster2.hp}"
        
        # Update bar colors
        if combat.monster1_hp / monster1.hp > 0.5:
            monster1_hp_bar.color = ft.Colors.GREEN
        elif combat.monster1_hp / monster1.hp > 0.25:
            monster1_hp_bar.color = ft.Colors.ORANGE
        else:
            monster1_hp_bar.color = ft.Colors.RED
            
        if combat.monster2_hp / monster2.hp > 0.5:
            monster2_hp_bar.color = ft.Colors.GREEN
        elif combat.monster2_hp / monster2.hp > 0.25:
            monster2_hp_bar.color = ft.Colors.ORANGE
        else:
            monster2_hp_bar.color = ft.Colors.RED
        
        # Update turn indicator
        turn_indicator.value = f"{combat.get_current_attacker().name}'s Turn"
        
        # Clear the current attacker's last roll display (ready for new roll)
        if combat.current_turn == 1:
            monster1_last_roll.value = ""
        else:
            monster2_last_roll.value = ""
        
        # Update combat log
        combat_log_column.controls = [
            ft.Text(log, size=TEXT_SIZE_SM, color=ft.Colors.GREY_300) 
            for log in combat.combat_log[-8:]  # Show last 8 messages
        ]
        
        # Update probability displays
        update_probability_display()
        
        page.update()
    
    def show_statistics(winner: Monster):
        """Show detailed battle statistics."""
        stats = combat.get_battle_statistics()
        
        stats_container.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("📊 Battle Statistics", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
                    ft.Divider(height=1, color=ft.Colors.GREY_700),
                    
                    # Monster 1 stats
                    ft.Text(f"{monster1.name}:", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
                    ft.Text(
                        f"Hit Rate: {stats['monster1']['actual_hit_rate']*100:.1f}% "
                        f"(expected {stats['monster1']['expected_hit_rate']*100:.1f}%)",
                        size=11, color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        f"Crit Rate: {stats['monster1']['actual_crit_rate']*100:.1f}% "
                        f"(expected {stats['monster1']['expected_crit_rate']*100:.1f}%)",
                        size=11, color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        f"Avg Damage Per Hit: {stats['monster1']['actual_avg_damage']:.1f} "
                        f"(expected {stats['monster1']['expected_avg_damage']:.1f})",
                        size=11, color=ft.Colors.WHITE
                    ),
                    ft.Container(height=5),
                    
                    # Monster 2 stats
                    ft.Text(f"{monster2.name}:", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ft.Text(
                        f"Hit Rate: {stats['monster2']['actual_hit_rate']*100:.1f}% "
                        f"(expected {stats['monster2']['expected_hit_rate']*100:.1f}%)",
                        size=11, color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        f"Crit Rate: {stats['monster2']['actual_crit_rate']*100:.1f}% "
                        f"(expected {stats['monster2']['expected_crit_rate']*100:.1f}%)",
                        size=11, color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        f"Avg Damage Per Hit: {stats['monster2']['actual_avg_damage']:.1f} "
                        f"(expected {stats['monster2']['expected_avg_damage']:.1f})",
                        size=11, color=ft.Colors.WHITE
                    ),
                    ft.Container(height=5),
                    
                    # General stats
                    ft.Text(f"Total Turns: {stats['general']['total_turns']}", size=11, color=ft.Colors.GREY_400),
                    ft.Text(
                        f"Average d20 roll: {stats['general']['average_roll']:.2f} (expected 10.5)",
                        size=11, color=ft.Colors.GREY_400
                    ),
                    ft.Container(height=10),
                    
                    # Rematch button
                    ft.ElevatedButton(
                        "⚔️ REMATCH",
                        width=150,
                        height=40,
                        on_click=lambda e: rematch(),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                        ),
                    ),
                ],
                spacing=3,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLACK38,
            border=ft.border.all(2, ft.Colors.AMBER_400),
            border_radius=10,
            padding=15,
            width=350,
        )
        stats_container.visible = True
    
    def show_victory(winner: Monster):
        """Show victory screen with statistics."""
        attack_button.disabled = True
        turn_indicator.value = f"🏆 {winner.name} WINS! 🏆"
        turn_indicator.color = ft.Colors.AMBER_400
        combat.combat_log.append("")
        combat.combat_log.append("====== BATTLE OVER ======")
        combat.combat_log.append(f"🏆 {winner.name} is victorious!")
        show_statistics(winner)
        update_ui()
    
    def rematch():
        """Restart the battle with the same monsters."""
        page.clean()
        page.add(battle_screen(page, monster1_index, monster2_index, on_back))
        page.update()
    
    def on_attack_click(e):
        """Handle attack button click."""
        hit, damage, message, attack_roll, damage_rolls, damage_dice_str = combat.perform_attack()
        
        # Display the dice rolls for the attacker
        is_monster1 = (combat.current_turn == 1)
        
        # Format the roll display with raw dice values
        attack_display = f"Attack: d20 → {attack_roll}"
        
        if hit:
            # Parse damage dice to show formula
            if attack_roll == 20:
                # On crit, show that dice were doubled
                num_dice, die_size, modifier = combat.get_current_attacker().damage_dice_parsed
                crit_dice_str = f"{num_dice * 2}d{die_size}{'+' + str(modifier) if modifier >= 0 else modifier}"
                damage_display = f"Damage: {crit_dice_str} → {damage_rolls} = {damage} (CRIT: doubled dice!)"
                roll_display = f"🎯 {attack_display} (CRIT!)\n{damage_display}"
            else:
                damage_display = f"Damage: {damage_dice_str} → {damage_rolls} = {damage}"
                roll_display = f"⚔️ {attack_display}\n{damage_display}"
        else:
            if attack_roll == 1:
                roll_display = f"💨 {attack_display} (AUTO-MISS)"
            else:
                roll_display = f"❌ {attack_display} (miss)"
        
        # Update the appropriate monster's last roll display
        if is_monster1:
            monster1_last_roll.value = roll_display
            monster1_last_roll.color = ft.Colors.AMBER_300 if hit else ft.Colors.RED_300
        else:
            monster2_last_roll.value = roll_display
            monster2_last_roll.color = ft.Colors.BLUE_300 if hit else ft.Colors.RED_300
        
        is_over, winner = combat.is_battle_over()
        
        if is_over:
            update_ui()
            show_victory(winner)
        else:
            combat.switch_turn()
            update_ui()
    
    def on_monte_carlo_click(e):
        """Handle Monte Carlo simulation button click."""
        from screens.monte_carlo_screen import monte_carlo_screen
        page.clean()
        page.add(monte_carlo_screen(page, monster1_index, monster2_index, on_back=lambda e: rematch()))
    
    attack_button.on_click = on_attack_click
    monte_carlo_button.on_click = on_monte_carlo_click
    
    # Initialize displays
    update_probability_display()
    
    # Helper function to create desktop monster card (vertical layout for side panels)
    def create_monster_card(monster: Monster, hp_bar, hp_text, last_roll_text, prob_container, color, is_left=True):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        monster.name,
                        size=TEXT_SIZE_XL,
                        weight=ft.FontWeight.BOLD,
                        color=color,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=SPACING_SM),
                    ft.Image(
                        src=monster.image_url if monster.image_url else "",
                        width=180,
                        height=180,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Icon(ft.Icons.QUESTION_MARK, size=90, color=ft.Colors.GREY_600),
                    ),
                    ft.Container(height=SPACING_SM),
                    hp_text,
                    ft.Container(height=SPACING_XS),
                    hp_bar,
                    ft.Container(height=SPACING_SM),
                    # Last roll display
                    last_roll_text,
                    ft.Container(height=SPACING_SM),
                    # Attack probabilities (shown when this monster's turn)
                    prob_container,
                    ft.Container(height=SPACING_SM),
                    # Monster stats display (simplified)
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    f"Attack Bonus: +{monster.attack_bonus}",
                                    size=TEXT_SIZE_SM,
                                    color=ft.Colors.CYAN_300,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"Defense (AC): {monster.ac}",
                                    size=TEXT_SIZE_SM,
                                    color=ft.Colors.BLUE_300,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"Damage: {monster.damage_dice}",
                                    size=TEXT_SIZE_SM,
                                    color=ft.Colors.ORANGE_300,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=SPACING_XS,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=10,
                        bgcolor=ft.Colors.BLACK26,
                        border_radius=5,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=SPACING_XS,
            ),
            padding=SPACING_SM,
            border=ft.border.all(2, color),
            border_radius=10,
            width=320,  # Reduced from MONSTER_CARD_WIDTH (380) to fit better
            bgcolor=ft.Colors.GREY_800,
        )
    
    # Create center panel with combat information
    center_panel = ft.Container(
        content=ft.Column(
            [
                # Compact header: Turn indicator + back button
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_size=20,
                            icon_color=ft.Colors.WHITE,
                            on_click=on_back,
                            tooltip="Back to Monster Selection",
                        ),
                        turn_indicator,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=SPACING_SM),
                # Combat Log
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "📜 Combat Log",
                                size=TEXT_SIZE_MD,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_400,
                            ),
                            ft.Container(
                                content=combat_log_column,
                                bgcolor=ft.Colors.BLACK26,
                                border_radius=5,
                                padding=8,
                                width=400,  # Fixed width prevents collapse when empty
                            ),
                        ],
                        spacing=SPACING_XS,
                    ),
                ),
                ft.Container(height=SPACING_SM),
                # Action buttons
                ft.Row(
                    [
                        attack_button,
                        monte_carlo_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=SPACING_SM,
                ),
                ft.Container(height=SPACING_SM),
                # Statistics container (shown after battle)
                stats_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,  # Make center panel flexible to take available space
        padding=SPACING_SM,
    )
    
    # Create horizontal 3-column layout with proper sizing
    return ft.Container(
        content=ft.Row(
            [
                # Left panel - Monster 1
                create_monster_card(monster1, monster1_hp_bar, monster1_hp_text, monster1_last_roll, m1_prob_container, ft.Colors.AMBER_400, is_left=True),
                # Center panel - Combat info (flexible)
                center_panel,
                # Right panel - Monster 2
                create_monster_card(monster2, monster2_hp_bar, monster2_hp_text, monster2_last_roll, m2_prob_container, ft.Colors.BLUE_400, is_left=False),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=SPACING_SM,  # Reduced spacing from SPACING_LG
            scroll=ft.ScrollMode.AUTO,  # Add horizontal scroll as fallback
        ),
        padding=SPACING_SM,  # Reduced padding from SPACING_LG
        expand=True,
    )
