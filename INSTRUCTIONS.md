# D&D Combat Simulator — Student Instructions

> **Note for students:** Your instructor will tell you how to get your own copy of this
> repository (e.g. a GitHub Classroom link or a fork) and will give you the specific
> deadline, grading weights, and whether you work solo or in pairs. This file describes
> *what to build*; your instructor supplies the *when* and *how it's graded*.

## Overview

You'll bring a Dungeons & Dragons 5e combat simulator to life by implementing its
**dice rolling** and **probability** math. The app already runs — it just produces wrong
numbers until you fill in the missing pieces. As you complete each phase, more of the
test suite passes and the simulator's results become correct.

By the end you will have practiced:
- **Randomness** — generating random dice rolls and testing them statistically
- **Probability** — hit chances, expected damage, critical hits
- **Conditional probability** — `P(crit | hit)` vs `P(crit)`
- **OOP & testing** — reading a class and writing `pytest` tests for it

---

## Project structure

```
├── utils/
│   ├── dice_roller.py          # Phase 1: YOU IMPLEMENT — random dice rolling
│   └── dice_parser.py          # Framework — parses dice notation, e.g. "2d6+3"
├── models/
│   └── monster.py              # Framework — Monster data model (you read this in Phase 4)
├── screens/                    # Framework — the app's UI (home, battle, selection, Monte Carlo)
├── tests/
│   ├── test_dice_roller.py     # Phase 1: YOU ADD TESTS
│   ├── test_probability.py     # Framework — tests your probability functions
│   ├── test_monster.py         # Phase 4: YOU COMPLETE
│   └── test_student_integration.py  # Framework — final validation (21 tests)
├── probability.py              # Phase 2 & 3: YOU IMPLEMENT
├── combat_system.py            # Framework — battle mechanics and turn logic
├── battle_simulator.py         # Framework — runs many battles (Monte Carlo)
├── dnd_api.py                  # Framework — fetches monster data from the D&D 5e API
├── main.py                     # Framework — app entry point
└── requirements.txt            # Dependencies
```

### What you may edit

**✅ Edit only these four files:**
- `utils/dice_roller.py` — implement dice rolling functions
- `probability.py` — implement probability calculations
- `tests/test_dice_roller.py` — add your own tests
- `tests/test_monster.py` — fill in missing values and complete tests

**❌ Do not edit** any other file. If you think you need to change framework code, ask your
instructor first.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configure API access

The app fetches monster data from the free, public [D&D 5e API](https://www.dnd5eapi.co/)
(no key needed). Copy the example config into a real `.env` file in the repository root:

```bash
cp .env.example .env
```

That file contains:

```
DND_API_BASE_URL=https://www.dnd5eapi.co/api/2014
DND_API_IMAGE_BASE_URL=https://www.dnd5eapi.co
```

📚 **Why isn't `.env` committed?** It's best practice to **never** commit `.env` files,
because they often hold secrets (API keys, passwords, database credentials). Even though
these URLs are public, you're practicing the proper workflow. Look at `.gitignore` — `.env`
is listed there, so Git ignores it and it never gets pushed.

### Run the app and tests

```bash
flet run main.py     # launch the simulator
pytest               # run all tests (some fail until you implement — that's expected)
```

---

## Your tasks

Complete the four phases **in order**.

### Phase 1 — Randomness
**File:** `utils/dice_roller.py`

Implement three functions:
- `roll_d20()` — roll a single d20
- `roll_dice(num_dice, die_size)` — roll multiple dice
- `roll_with_modifier(num_dice, die_size, modifier)` — roll dice and apply a modifier

Then add tests in `tests/test_dice_roller.py` (follow the `TODO` comments — these are
*statistical* tests: a fair die should, over many rolls, land in range and average out).

**Verify:** `pytest tests/test_dice_roller.py -v`

### Phase 2 — Basic probability
**File:** `probability.py`

Implement (formulas are given in the comments above each function):
- `calculate_hit_probability(attack_bonus, target_ac)` — `P(attack hits)`
- `calculate_expected_damage(num_dice, die_size, modifier)` — `E[damage]`
- `calculate_min_roll_needed(attack_bonus, target_ac)` — minimum d20 needed to hit
- `calculate_damage_range(num_dice, die_size, modifier)` — `(min, max)` damage

`calculate_crit_probability()` is already implemented as a worked example.

**Verify:** `pytest tests/test_probability.py -v`

### Phase 3 — Conditional probability
**File:** `probability.py`

Implement two advanced functions:
- `calculate_crit_given_hit(...)` — `P(crit | hit)`, a conditional probability
- `calculate_expected_damage_per_attack(...)` — expected damage accounting for misses

Note: `P(crit | hit)` is **higher** than the raw 5% crit rate — make sure you understand
why.

**Verify:** `pytest tests/test_probability.py -v` (all should pass now)

### Phase 4 — OOP & testing
**File:** `tests/test_monster.py`

Read `models/monster.py` to understand the `Monster` class, then:
- Fill in the missing expected values (replace the `-1` placeholders with correct attack
  bonuses)
- Complete the two test functions at the end of the file

**Verify:** `pytest tests/test_monster.py -v`

---

## Success criteria (core track)

You're done with the coding portion when:
1. `pytest tests/test_student_integration.py` shows **21/21 passing**
2. `flet run main.py` runs without errors
3. The battle screen shows correct probability calculations
4. The Monte Carlo simulator produces accurate, stabilizing results

---

## Optional: Advanced / Math track

*Your instructor will tell you whether this track is required for you.*

Use the working simulator to connect theory to evidence: pick monster matchups, compute
their probabilities by hand, then run Monte Carlo simulations and compare.

1. **Select 5 matchups** with variety — e.g. evenly matched, a clear favorite, glass
   cannon vs. tank, two weak monsters, and a wildcard of your choice.
2. **Calculate by hand**, for each monster in each pair:
   - **Hit probability:** `P(hit) = (21 − needed_roll) / 20`, clamped to `[0.05, 0.95]`
   - **Expected damage per hit:** `E = num_dice × (die_size + 1) / 2 + modifier`
   - **Expected damage per attack:** `P(hit) × E[damage | hit]`
   - **Conditional crit:** `P(crit | hit) = 0.05 / P(hit)`
3. **Simulate** each matchup at **three sample sizes** (e.g. 100, 1000, 5000 battles) and
   record win rates, average rounds, hit rates, crit rates, and average damage.
4. **Analyze** (1–2 paragraphs per matchup): How close were your hand calculations to the
   simulation? Did the predicted winner win? How did results change with sample size? Did
   you see the Law of Large Numbers in action? What surprised you?

Submit your write-up in the format your instructor specifies (e.g. a PDF with your chosen
pairs, hand calculations, simulation data tables, and analysis).

---

## Tips

1. **Start with Phase 1.** Dice rolling is the foundation everything else builds on.
2. **Read the formulas** in the comments above each function.
3. **Run tests often** — let them guide your implementation.
4. **Use the app** — `flet run main.py` shows your code working (or not).
5. **Probability is tricky on purpose** — conditional probability especially. Ask
   questions and pair up on the hard functions.
6. **Preserve the type hints** in every function you implement.

Good luck, and may the dice roll in your favor! 🎲
