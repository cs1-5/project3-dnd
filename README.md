# D&D Combat Simulator — Probability & Testing Project

A ready-to-assign programming project that teaches **discrete probability, randomness,
object-oriented programming, and software testing** through a Dungeons & Dragons 5e
combat simulator. Students implement dice rolling and probability functions inside a
working [Flet](https://flet.dev) desktop app, then compare their hand-calculated
probabilities against Monte Carlo simulation.

> **For educators.** This repository contains the **starter code only** — the scaffolding
> students receive. It is designed to be adopted as-is, adapted, or used as a reference.
> Reference solutions are **not** included in this public repo (see
> [Getting the solution](#getting-the-solution)).

---

## Why this project works in the classroom

This assignment is described and evaluated in the accompanying paper:

> **[Teaching Probability Through Game Simulation](https://arxiv.org/abs/2604.16365)**
> (arXiv:2604.16365)

The core idea: students don't just compute probabilities on paper — they implement them,
watch a real application use their code, and then *empirically verify* their math against
thousands of simulated battles. The Law of Large Numbers stops being an abstraction.

## What students learn

| Theme | Concepts |
|-------|----------|
| **Randomness** | Pseudo-random generation, statistical (Law of Large Numbers) testing |
| **Discrete probability** | Hit probability, expected value, damage ranges, critical-hit odds |
| **Conditional probability** | `P(crit \| hit)` vs `P(crit)`, expected value with compounding factors |
| **OOP** | Classes, computed properties, validation, caching |
| **Testing** | Unit tests, statistical tests, integration tests with `pytest` |

## How the project is scaffolded

Students work through four phases, editing **only four files**; everything else is a
working framework they read but don't modify.

| Phase | Student edits | Skill |
|-------|---------------|-------|
| 1. Randomness | `utils/dice_roller.py`, `tests/test_dice_roller.py` | Random generation + statistical tests |
| 2. Basic probability | `probability.py` | Hit chance, expected damage, damage range |
| 3. Conditional probability | `probability.py` | `P(crit\|hit)`, expected damage per attack |
| 4. OOP & testing | `tests/test_monster.py` | Reading a class, writing validation tests |

The starter functions ship as stubs returning **dummy values** clearly marked
`# DUMMY VALUE`, so the application *runs* from day one (it just shows wrong numbers
until students fill in the math). A suite of integration tests
(`tests/test_student_integration.py`) goes from failing to passing as students progress —
useful as both a student progress signal and an autograder hook.

Full step-by-step student-facing directions are in **[INSTRUCTIONS.md](INSTRUCTIONS.md)**.

## Project layout

```
.
├── INSTRUCTIONS.md          # Student-facing assignment (hand this to students)
├── main.py                  # App entry point (framework)
├── probability.py           # Phase 2 & 3: students implement
├── combat_system.py         # Turn-based battle logic (framework)
├── battle_simulator.py      # Monte Carlo runner (framework)
├── dnd_api.py               # Fetches monster data from the D&D 5e API (framework)
├── models/monster.py        # Monster data model (framework; read in Phase 4)
├── screens/                 # Flet UI (framework)
├── utils/
│   ├── dice_roller.py       # Phase 1: students implement
│   └── dice_parser.py       # Dice-notation parser, e.g. "2d6+3" (framework)
└── tests/                   # pytest suite (students add to test_dice_roller & test_monster)
```

## Quick start (instructor smoke test)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # point the app at the D&D 5e API
flet run main.py                 # launch the app
pytest                           # run the test suite (some fail until implemented — expected)
```

The app fetches monster stats from the free, public
[D&D 5e API](https://www.dnd5eapi.co/) — no API key required.

## Adopting this in your course

This repo is intentionally course-agnostic. The pieces below are **examples to adapt**,
not requirements:

- **Pairs / solo.** Written assuming pair work, but works fine solo.
- **Deadlines, rubrics, course numbers.** [INSTRUCTIONS.md](INSTRUCTIONS.md) keeps an
  optional **"Advanced / Math track"** (a hand-calculation + Monte Carlo write-up) on top
  of the **"Core / Code track."** Drop the math track, change point values, or merge them
  to fit your course.
- **Distribution.** Use this repo as a **GitHub template** (Settings → *Template repository*)
  or as a [GitHub Classroom](https://classroom.github.com/) assignment source so each
  student/team gets their own copy.
- **`.env`.** Deliberately git-ignored and shipped as `.env.example` to teach the "never
  commit secrets" habit, even though these particular URLs are public.

## Getting the solution

To keep this assignment usable, the reference implementation is **not** published here.
Educators can request it — see the contact details in the
[paper](https://arxiv.org/abs/2604.16365), or open an issue in the
[cs1-5](https://github.com/cs1-5) organization.

## Authors

- Ildar Akhmetov ([@ildarakhmetov](https://github.com/ildarakhmetov))
- Juancho Buchanan ([@sillyfunnypedro](https://github.com/sillyfunnypedro))

## License

Released under [**CC0 1.0 Universal**](LICENSE) — effectively public domain. You may copy,
modify, and reuse this material for any purpose, commercial or not, with no attribution
required. Attribution is always appreciated but never obligatory.

> Note: D&D content fetched at runtime comes from the [D&D 5e API](https://www.dnd5eapi.co/)
> and is governed by the [Open Game License / SRD](https://www.dnd5eapi.co/), independent
> of this repository's CC0 dedication.
