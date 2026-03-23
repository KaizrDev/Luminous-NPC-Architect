# Luminous Game Architect

Luminous is a comprehensive Agent Skill for Claude Code designed to streamline the game development lifecycle. It provides a unified framework for systems architecture, asset pipeline automation, and formal logic validation.

## Features

- **Project Scaffolding:** Automated creation of engine-standard directory structures and boilerplate.
- **Asset Pipeline:** Generation of metadata and organizational plans for 2D and 3D assets.
- **Logic Validation:** A built-in Python suite to verify Finite State Machines (FSM) for NPC behavior and game rules.
- **Cross-Engine Support:** Optimized for Unity (C#), Godot (GDScript), and Python-based frameworks.

## Installation

1. Clone the repository into your project root:
   ```bash
   git clone [https://github.com/KaizrDev/Luminous-NPC-Architect.git]
   ```
2. Activate the skill in your Claude Code environment.

## Usage

### Core Commands

- **`/luminous-init`**: Scaffolds a new game project with a clean architecture.
- **`/luminous-npc`**: Generates a validated FSM logic file for an NPC.
- **`/luminous-asset`**: Creates a metadata file or directory plan for a new asset.

### Logic Validation

To ensure your game logic is free of dead-ends, use the internal Python validator:

```bash
python scripts/luminous_verify.py --type [fsm|dir] [path]
```

- **`--type fsm`**: Validates a Finite State Machine JSON file.
- **`--type dir`**: Validates the project directory structure.

## Architecture Principles

Luminous enforces a **Decoupled Architecture** where game logic is separated from the rendering engine. This ensures:
- **Maintainability**: Changes to the UI or rendering pipeline do not break core gameplay logic.
- **Performance**: Logic can be optimized independently of visual assets.
- **Scalability**: The codebase remains organized as the project grows.

## License

MIT