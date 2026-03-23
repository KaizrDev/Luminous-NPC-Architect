---
description: Scaffolds a new game project with a clean, decoupled architecture. Supports Unity, Godot, and Python/Pygame.
---

# /luminous-init

Scaffolds a new game project directory structure based on the target engine.

## Steps

1. **Ask the user** for the following information if not already provided:
   - **Project Name**: The name of the game project (e.g., `my-rpg-game`).
   - **Target Engine**: One of `unity`, `godot`, or `python`.

2. **Create the root project directory** using the project name.

3. **Generate the engine-specific directory structure.** Create all directories and placeholder files.

   ### For `unity` (C#):
   ```
   <project-name>/
   ├── Assets/
   │   ├── Scripts/
   │   │   ├── Core/          # Game managers, singletons
   │   │   ├── Entities/      # Player, NPC, enemy scripts
   │   │   ├── Systems/       # ECS systems, AI controllers
   │   │   └── UI/            # HUD, menus, dialogs
   │   ├── Prefabs/
   │   ├── Scenes/
   │   ├── Materials/
   │   ├── Textures/
   │   │   ├── Characters/
   │   │   ├── Environment/
   │   │   └── UI/
   │   ├── Audio/
   │   │   ├── SFX/
   │   │   └── Music/
   │   └── Animations/
   ├── docs/
   │   └── DESIGN.md
   └── README.md
   ```

   ### For `godot` (GDScript):
   ```
   <project-name>/
   ├── src/
   │   ├── core/              # Autoloads, game manager
   │   ├── entities/          # Player, NPC scenes + scripts
   │   ├── systems/           # AI, physics, state machines
   │   └── ui/                # HUD, menus
   ├── assets/
   │   ├── textures/
   │   │   ├── characters/
   │   │   ├── environment/
   │   │   └── ui/
   │   ├── audio/
   │   │   ├── sfx/
   │   │   └── music/
   │   └── fonts/
   ├── scenes/
   │   ├── levels/
   │   └── ui/
   ├── scripts/
   ├── docs/
   │   └── DESIGN.md
   └── README.md
   ```

   ### For `python` (Pygame / generic):
   ```
   <project-name>/
   ├── src/
   │   ├── core/              # Game loop, managers
   │   │   └── __init__.py
   │   ├── entities/          # Player, NPCs, enemies
   │   │   └── __init__.py
   │   ├── systems/           # AI, physics, collision
   │   │   └── __init__.py
   │   └── ui/                # Menus, HUD rendering
   │       └── __init__.py
   ├── assets/
   │   ├── textures/
   │   │   ├── characters/
   │   │   ├── environment/
   │   │   └── ui/
   │   ├── audio/
   │   │   ├── sfx/
   │   │   └── music/
   │   └── fonts/
   ├── scripts/
   ├── docs/
   │   └── DESIGN.md
   ├── tests/
   │   └── __init__.py
   ├── requirements.txt
   ├── main.py
   └── README.md
   ```

4. **Generate boilerplate files** inside the structure:

   - **`README.md`**: A starter README with project name, engine, and basic usage section.
   - **`docs/DESIGN.md`**: A design document template with sections for:
     - Game Overview
     - Core Mechanics
     - Systems Architecture (ECS or MVC decision)
     - Art & Audio Pipeline
     - Milestone Roadmap

   - **Engine-specific entry point:**
     - `unity`: Create a `GameManager.cs` stub in `Assets/Scripts/Core/`.
     - `godot`: Create a `game_manager.gd` autoload stub in `src/core/`.
     - `python`: Create a `main.py` with a basic Pygame game loop skeleton.

5. **Run the directory validator** to confirm structure:
   ```bash
   python scripts/luminous_verify.py --type dir <project-name>
   ```

6. **Report the result** to the user, including:
   - The full directory tree.
   - Any validation warnings.
   - Suggested next steps (e.g., "Use `/luminous-npc` to add an NPC with validated AI.").
