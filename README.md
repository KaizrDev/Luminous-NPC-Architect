# Luminous Game Architect

A comprehensive Agent Skill for AI-powered code editors designed to streamline the game development lifecycle. Provides a unified framework for systems architecture, asset pipeline automation, and formal logic validation.

## Features

- **Project Scaffolding:** Automated creation of engine-standard directory structures and boilerplate.
- **NPC AI Generation:** Create validated FSM and Behavior Tree logic for NPCs with automatic dead-end detection.
- **Asset Pipeline:** Generation of metadata and organizational plans for 2D and 3D assets.
- **Logic Validation:** A built-in Python suite to verify FSMs, Behavior Trees, and project structure.
- **Cross-Engine Support:** Optimized for Unity (C#), Godot (GDScript), and Python-based frameworks.

## Installation

1. Clone the repository into your project root:
   ```bash
   git clone https://github.com/KaizrDev/Luminous-NPC-Architect.git
   ```
2. The `.agent/workflows/` directory will auto-register the slash commands in your AI coding environment.

## Usage

### Slash Commands

| Command | Description |
|---------|-------------|
| `/luminous-init` | Scaffold a new game project with engine-specific architecture. |
| `/luminous-npc` | Generate a validated FSM or Behavior Tree for an NPC. |
| `/luminous-asset` | Create asset metadata files, directory plans, or pipeline roadmaps. |

### Logic Validation (CLI)

Validate your game logic directly from the terminal:

```bash
# Validate an FSM JSON file
python scripts/luminous_verify.py --type fsm path/to/npc_ai.json

# Validate a Behavior Tree JSON file
python scripts/luminous_verify.py --type bt path/to/boss_ai.json

# Validate a project directory structure
python scripts/luminous_verify.py --type dir path/to/project
```

### Examples

The `examples/` directory contains reference files you can test with:

```bash
python scripts/luminous_verify.py --type fsm examples/guard_fsm.json
python scripts/luminous_verify.py --type bt examples/boss_dragon_bt.json
```

## Project Structure

```
Luminous-NPC-Architect/
├── .agent/
│   └── workflows/
│       ├── luminous-init.md      # Project scaffolding workflow
│       ├── luminous-npc.md       # NPC AI generation workflow
│       └── luminous-asset.md     # Asset metadata workflow
├── scripts/
│   └── luminous_verify.py        # CLI validation tool
├── examples/
│   ├── guard_fsm.json            # Example FSM (6-state guard)
│   └── boss_dragon_bt.json       # Example Behavior Tree (dragon boss)
├── SKILLS.md                     # Skill definition
├── README.md
└── LICENSE
```

## Architecture Principles

Luminous enforces a **Decoupled Architecture** where game logic is separated from the rendering engine:

- **Maintainability**: Changes to the UI or rendering pipeline do not break core gameplay logic.
- **Performance**: Logic can be optimized independently of visual assets.
- **Scalability**: The codebase remains organized as the project grows.
- **Portability**: Clean separation enables engine migration with minimal rewrites.

## License

MIT