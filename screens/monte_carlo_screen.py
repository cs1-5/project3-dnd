"""
Monte Carlo Simulation Screen

Educational screen teaching Monte Carlo simulation through battle simulations.
Demonstrates Law of Large Numbers with live convergence visualization.
"""

import flet as ft
from dnd_api import get_monster_details
from battle_simulator import run_multiple_battles_with_callback
from probability import (
    calculate_hit_probability,
    calculate_expected_damage,
    calculate_crit_probability
)
from ui_constants import (
    TEXT_SIZE_XL, TEXT_SIZE_LG, TEXT_SIZE_MD, TEXT_SIZE_SM,
    SPACING_LG, SPACING_MD, SPACING_SM, SPACING_XS
)


def monte_carlo_screen(page: ft.Page, monster1_index: str, monster2_index: str, on_back):
    """
    Interactive Monte Carlo simulation screen.
    
    Teaches students about:
    - Monte Carlo method
    - Law of Large Numbers
    - Convergence of estimates
    """
    
    # Load monsters
    monster1 = get_monster_details(monster1_index)
    monster2 = get_monster_details(monster2_index)
    
    if not monster1 or not monster2:
        page.add(ft.Text("Error loading monsters"))
        return
    
    # UI Components
    setup_container = ft.Container()
    simulation_container = ft.Container(visible=False)
    results_container = ft.Container(visible=False)
    
    # Progress components
    progress_ring = ft.ProgressRing(width=60, height=60, stroke_width=4)
    progress_text = ft.Text("", size=TEXT_SIZE_LG, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_400)
    progress_bar = ft.ProgressBar(width=300, height=10, value=0)
    
    # Current results display
    current_m1_wins_text = ft.Text("", size=TEXT_SIZE_MD)
    current_m2_wins_text = ft.Text("", size=TEXT_SIZE_MD)
    
    # Convergence visualization (simple text-based bars)
    convergence_display = ft.Column([], spacing=SPACING_XS)
    
    # Final results display
    final_stats_column = ft.Column([], spacing=SPACING_SM)
    
    def create_ascii_bar(value: float, max_value: float = 1.0, width: int = 20) -> str:
        """Create a simple ASCII progress bar."""
        filled = int((value / max_value) * width)
        return "█" * filled + "░" * (width - filled)
    
    def update_convergence_display(history: list):
        """Update convergence visualization with latest data."""
        if len(history) < 2:
            return
        
        convergence_display.controls.clear()
        
        # Show title
        convergence_display.controls.append(
            ft.Text(
                f"Win Rate Convergence ({monster1.name})",
                size=TEXT_SIZE_MD,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.AMBER_400
            )
        )
        
        # Show key data points from history
        display_points = []
        if len(history) <= 8:
            display_points = history
        else:
            # Show start, middle points, and end
            indices = [0, len(history)//4, len(history)//2, 3*len(history)//4, -1]
            display_points = [history[i] for i in indices]
        
        for battles, win_rate in display_points:
            bar = create_ascii_bar(win_rate, 1.0, 20)
            
            # Status indicator based on sample size
            if battles >= 1000:
                status = "↓"
                status_color = ft.Colors.YELLOW_400
            else:
                status = "•"
                status_color = ft.Colors.GREY_400
            
            convergence_display.controls.append(
                ft.Row(
                    [
                        ft.Text(
                            f"[{battles:5d}]:",
                            size=TEXT_SIZE_SM,
                            color=ft.Colors.GREY_400,
                            font_family="Courier New",
                            width=80
                        ),
                        ft.Text(
                            bar,
                            size=TEXT_SIZE_SM,
                            color=ft.Colors.PURPLE_400,
                            font_family="Courier New"
                        ),
                        ft.Text(
                            f" {win_rate*100:5.1f}%",
                            size=TEXT_SIZE_SM,
                            color=ft.Colors.WHITE,
                            font_family="Courier New",
                            width=60
                        ),
                        ft.Text(
                            status,
                            size=TEXT_SIZE_MD,
                            color=status_color,
                            weight=ft.FontWeight.BOLD
                        ),
                    ],
                    spacing=5
                )
            )
    
    def update_callback(current_results: dict):
        """Called periodically during simulation to update UI."""
        completed = current_results['completed']
        total = current_results['total']
        m1_wins = current_results['monster1_wins']
        m2_wins = current_results['monster2_wins']
        m1_rate = current_results['monster1_win_rate']
        m2_rate = current_results['monster2_win_rate']
        avg_rounds = current_results.get('avg_turns', 0)
        history = current_results['win_rate_history']
        
        # Update progress
        progress_text.value = f"Running: {completed}/{total} battles... (avg: {avg_rounds:.1f} rounds)"
        progress_bar.value = completed / total
        
        # Update current results
        current_m1_wins_text.value = f"{monster1.name}: {m1_wins} wins ({m1_rate*100:.1f}%)"
        current_m1_wins_text.color = ft.Colors.AMBER_400
        
        current_m2_wins_text.value = f"{monster2.name}: {m2_wins} wins ({m2_rate*100:.1f}%)"
        current_m2_wins_text.color = ft.Colors.BLUE_400
        
        # Update convergence visualization
        update_convergence_display(history)
        
        page.update()
    
    def run_simulation(num_battles: int):
        """Run the simulation with live updates."""
        # Hide setup, show simulation
        setup_container.visible = False
        simulation_container.visible = True
        results_container.visible = False
        page.update()
        
        # Reset displays
        convergence_display.controls.clear()
        progress_bar.value = 0
        
        # Run simulation
        final_results = run_multiple_battles_with_callback(
            monster1_index,
            monster2_index,
            num_battles,
            update_callback=update_callback,
            update_frequency=max(1, num_battles // 50)  # ~50 updates
        )
        
        # Show final results
        show_final_results(final_results)
    
    def show_final_results(results: dict):
        """Display final statistics and insights."""
        simulation_container.visible = False
        results_container.visible = True
        
        total = results['total_battles']
        m1_wins = results['monster1_wins']
        m2_wins = results['monster2_wins']
        m1_rate = results['monster1_win_rate']
        m2_rate = results['monster2_win_rate']
        avg_rounds = results.get('avg_turns', 0)
        min_rounds = results.get('min_rounds', 0)
        max_rounds = results.get('max_rounds', 0)
        
        # Get aggregated statistics
        m1_hit_rate = results.get('monster1_avg_hit_rate', 0)
        m1_crit_rate = results.get('monster1_avg_crit_rate', 0)
        m1_dmg_per_hit = results.get('monster1_avg_dmg_per_hit', 0)
        m2_hit_rate = results.get('monster2_avg_hit_rate', 0)
        m2_crit_rate = results.get('monster2_avg_crit_rate', 0)
        m2_dmg_per_hit = results.get('monster2_avg_dmg_per_hit', 0)
        avg_d20 = results.get('avg_d20_roll', 0)
        total_rolls = results.get('total_d20_rolls', 0)
        
        # Calculate expected values for comparison
        m1_expected_hit_rate = calculate_hit_probability(monster1.attack_bonus, monster2.ac)
        m2_expected_hit_rate = calculate_hit_probability(monster2.attack_bonus, monster1.ac)
        
        num_dice_1, die_size_1, mod_1 = monster1.damage_dice_parsed
        num_dice_2, die_size_2, mod_2 = monster2.damage_dice_parsed
        m1_expected_dmg = calculate_expected_damage(num_dice_1, die_size_1, mod_1)
        m2_expected_dmg = calculate_expected_damage(num_dice_2, die_size_2, mod_2)
        
        expected_crit_rate = calculate_crit_probability()
        expected_d20 = 10.5
        
        # Build final stats display
        final_stats_column.controls.clear()
        
        final_stats_column.controls.extend([
            ft.Text(
                "📊 Final Statistics",
                size=TEXT_SIZE_XL,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.PURPLE_400
            ),
            ft.Container(height=SPACING_MD),
            
            ft.Text(
                f"Total Battles: {total:,}",
                size=TEXT_SIZE_LG,
                color=ft.Colors.WHITE
            ),
            ft.Container(height=SPACING_SM),
            
            # Monster 1 results
            ft.Text(
                monster1.name,
                size=TEXT_SIZE_MD,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.AMBER_400
            ),
            ft.Text(
                f"  Win Rate: {m1_rate*100:.1f}% ({m1_wins} wins)",
                size=TEXT_SIZE_MD,
                color=ft.Colors.WHITE,
                font_family="Courier New"
            ),
            ft.Container(height=SPACING_SM),
            
            # Monster 2 results
            ft.Text(
                monster2.name,
                size=TEXT_SIZE_MD,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_400
            ),
            ft.Text(
                f"  Win Rate: {m2_rate*100:.1f}% ({m2_wins} wins)",
                size=TEXT_SIZE_MD,
                color=ft.Colors.WHITE,
                font_family="Courier New"
            ),
            ft.Container(height=SPACING_MD),
            
            # Battle duration statistics
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "⏱️ Battle Duration (Rounds)",
                        size=TEXT_SIZE_MD,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_400
                    ),
                    ft.Container(height=SPACING_XS),
                    ft.Text(
                        f"  Average: {avg_rounds:.1f} rounds",
                        size=TEXT_SIZE_MD,
                        color=ft.Colors.WHITE,
                        font_family="Courier New"
                    ),
                    ft.Text(
                        f"  Shortest: {min_rounds} rounds",
                        size=TEXT_SIZE_MD,
                        color=ft.Colors.GREEN_300,
                        font_family="Courier New"
                    ),
                    ft.Text(
                        f"  Longest: {max_rounds} rounds",
                        size=TEXT_SIZE_MD,
                        color=ft.Colors.ORANGE_300,
                        font_family="Courier New"
                    ),
                ]),
                padding=10,
                bgcolor=ft.Colors.BLACK26,
                border_radius=5,
            ),
            ft.Container(height=SPACING_MD),
            
            # Law of Large Numbers - Convergence Statistics
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "📈 Law of Large Numbers in Action",
                        size=TEXT_SIZE_MD,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.CYAN_400
                    ),
                    ft.Text(
                        f"({total_rolls:,} total d20 rolls)",
                        size=TEXT_SIZE_SM,
                        color=ft.Colors.GREY_400,
                        italic=True
                    ),
                    ft.Container(height=SPACING_XS),
                    
                    # Average d20 roll
                    ft.Text(
                        f"Average d20 Roll: {avg_d20:.2f} (expected {expected_d20})",
                        size=TEXT_SIZE_MD,
                        color=ft.Colors.WHITE,
                        font_family="Courier New"
                    ),
                    ft.Container(height=SPACING_SM),
                    
                    # Monster 1 statistics
                    ft.Text(
                        f"{monster1.name}:",
                        size=TEXT_SIZE_SM,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.AMBER_400
                    ),
                    ft.Text(
                        f"  Hit Rate: {m1_hit_rate*100:.1f}% (expected {m1_expected_hit_rate*100:.1f}%)",
                        size=TEXT_SIZE_SM,
                        color=ft.Colors.WHITE,
                        font_family="Courier New"
                    ),
                    ft.Text(
                        f"  Crit Rate: {m1_crit_rate*100:.1f}% (expected {expected_crit_rate*100:.1f}%)",
                        size=TEXT_SIZE_SM,
                        color=ft.Colors.WHITE,
                        font_family="Courier New"
                    ),
                    ft.Text(
                        f"  Avg Dmg/Hit: {m1_dmg_per_hit:.1f} (expected {m1_expected_dmg:.1f})",
                        size=TEXT_SIZE_SM,
                        color=ft.Colors.WHITE,
                        font_family="Courier New"
                    ),
                    ft.Container(height=SPACING_XS),
                    
                    # Monster 2 statistics
                    ft.Text(
                        f"{monster2.name}:",
                        size=TEXT_SIZE_SM,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_400
                    ),
                    ft.Text(
                        f"  Hit Rate: {m2_hit_rate*100:.1f}% (expected {m2_expected_hit_rate*100:.1f}%)",
                        size=TEXT_SIZE_SM,
                        color=ft.Colors.WHITE,
                        font_family="Courier New"
                    ),
                    ft.Text(
                        f"  Crit Rate: {m2_crit_rate*100:.1f}% (expected {expected_crit_rate*100:.1f}%)",
                        size=TEXT_SIZE_SM,
                        color=ft.Colors.WHITE,
                        font_family="Courier New"
                    ),
                    ft.Text(
                        f"  Avg Dmg/Hit: {m2_dmg_per_hit:.1f} (expected {m2_expected_dmg:.1f})",
                        size=TEXT_SIZE_SM,
                        color=ft.Colors.WHITE,
                        font_family="Courier New"
                    ),
                ]),
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN_900),
                border=ft.border.all(2, ft.Colors.CYAN_400),
                border_radius=10,
            ),
        ])
        
        page.update()
    
    def reset_to_setup():
        """Return to setup screen."""
        setup_container.visible = True
        simulation_container.visible = False
        results_container.visible = False
        page.update()
    
    # Build Setup Screen
    setup_container.content = ft.Column(
        [
            ft.Text(
                "🎲 Monte Carlo Simulation",
                size=TEXT_SIZE_XL,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.PURPLE_400
            ),
            ft.Container(height=SPACING_MD),
            
            # Educational explanation
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "What is Monte Carlo Simulation?",
                            size=TEXT_SIZE_LG,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.AMBER_400
                        ),
                        ft.Container(height=SPACING_SM),
                        ft.Text(
                            "We run many random battles and count the wins. "
                            "The more battles we run, the more stable and accurate our results become "
                            "(Law of Large Numbers).",
                            size=TEXT_SIZE_SM,
                            color=ft.Colors.GREY_300
                        ),
                    ]
                ),
                padding=15,
                bgcolor=ft.Colors.BLACK26,
                border_radius=10,
            ),
            ft.Container(height=SPACING_MD),
            
            # Simulation size selection
            ft.Text(
                "How many battles to simulate?",
                size=TEXT_SIZE_LG,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE
            ),
            ft.Container(height=SPACING_SM),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "10",
                        on_click=lambda e: run_simulation(10),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700),
                    ),
                    ft.ElevatedButton(
                        "100",
                        on_click=lambda e: run_simulation(100),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_700),
                    ),
                    ft.ElevatedButton(
                        "1000",
                        on_click=lambda e: run_simulation(1000),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_800),
                    ),
                    ft.ElevatedButton(
                        "5000",
                        on_click=lambda e: run_simulation(5000),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.DEEP_PURPLE_900),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            ft.Container(height=SPACING_MD),
            
            # Back button
            ft.ElevatedButton(
                "← Back to Battle",
                on_click=on_back,
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    
    # Build Simulation Screen (shown during running)
    simulation_container.content = ft.Column(
        [
            ft.Container(height=SPACING_LG),
            progress_ring,
            ft.Container(height=SPACING_MD),
            progress_text,
            ft.Container(height=SPACING_SM),
            progress_bar,
            ft.Container(height=SPACING_MD),
            ft.Text(
                "Current Results:",
                size=TEXT_SIZE_LG,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE
            ),
            ft.Container(height=SPACING_SM),
            current_m1_wins_text,
            current_m2_wins_text,
            ft.Container(height=SPACING_MD),
            convergence_display,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    
    # Build Results Screen (shown after completion)
    results_container.content = ft.Column(
        [
            final_stats_column,
            ft.Container(height=SPACING_MD),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Run Again",
                        on_click=lambda e: reset_to_setup(),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_700),
                    ),
                    ft.ElevatedButton(
                        "← Back to Battle",
                        on_click=on_back,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    
    # Main container
    main_container = ft.Container(
        content=ft.Column(
            [
                setup_container,
                simulation_container,
                results_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        expand=True,
    )
    
    return main_container

