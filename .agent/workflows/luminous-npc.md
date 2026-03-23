---
description: Generates a validated Finite State Machine (FSM) or Behavior Tree logic file for an NPC, with automatic dead-end detection.
---

# /luminous-npc

Generates an NPC AI logic definition as a validated JSON FSM or Behavior Tree.

## Steps

1. **Ask the user** for the following information if not already provided:
   - **NPC Name**: The name/type of the NPC (e.g., `guard`, `shopkeeper`, `dragon`).
   - **Behavior Type**: One of `fsm` (Finite State Machine) or `behavior-tree`.
   - **Target Engine**: One of `unity`, `godot`, or `python` (determines script output format).
   - **Behavior Description** (optional): A natural language description of the NPC's behaviors (e.g., "patrols between points, chases player on sight, returns to patrol after 10s").

2. **Design the AI logic** based on the NPC description.

   ### For `fsm` type:

   Create a JSON file following this schema:
   ```json
   {
     "npc": "<npc_name>",
     "type": "fsm",
     "initial_state": "<starting_state>",
     "states": [
       {
         "name": "idle",
         "description": "NPC is stationary and waiting.",
         "actions": ["play_idle_animation"]
       },
       {
         "name": "patrol",
         "description": "NPC moves between waypoints.",
         "actions": ["move_to_next_waypoint", "play_walk_animation"]
       }
     ],
     "transitions": [
       {
         "from": "idle",
         "to": "patrol",
         "condition": "timer_expired(3.0)"
       },
       {
         "from": "patrol",
         "to": "chase",
         "condition": "player_in_range(10.0)"
       },
       {
         "from": "chase",
         "to": "patrol",
         "condition": "player_out_of_range(15.0)"
       }
     ]
   }
   ```

   ### For `behavior-tree` type:

   Create a JSON file following this schema:
   ```json
   {
     "npc": "<npc_name>",
     "type": "behavior_tree",
     "root": {
       "type": "selector",
       "children": [
         {
           "type": "sequence",
           "name": "combat_behavior",
           "children": [
             { "type": "condition", "name": "is_enemy_visible" },
             { "type": "condition", "name": "is_health_above", "params": { "threshold": 0.3 } },
             { "type": "action", "name": "attack_enemy" }
           ]
         },
         {
           "type": "sequence",
           "name": "flee_behavior",
           "children": [
             { "type": "condition", "name": "is_health_below", "params": { "threshold": 0.3 } },
             { "type": "action", "name": "flee_from_enemy" }
           ]
         },
         {
           "type": "action",
           "name": "patrol"
         }
       ]
     }
   }
   ```

3. **Save the JSON file** to the project:
   - Path: `src/entities/<npc_name>_ai.json` (Godot/Python) or `Assets/Scripts/Entities/<NpcName>AI.json` (Unity).

4. **Validate the logic** using the built-in verifier:
   ```bash
   python scripts/luminous_verify.py --type fsm <path_to_json>
   ```
   - If validation **fails** (dead-end states detected), fix the transitions automatically and re-validate.
   - Repeat until validation passes.

5. **Generate an engine-specific script** that implements the FSM/BT:

   - **Unity (C#):** Generate a `<NpcName>AI.cs` MonoBehaviour with an enum for states and a `switch` statement in `Update()`.
   - **Godot (GDScript):** Generate a `<npc_name>_ai.gd` script with `match` statement-based state handling.
   - **Python:** Generate a `<npc_name>_ai.py` class with a dictionary-based state machine.

6. **Report the result** to the user, including:
   - The FSM/BT diagram as a text-based visualization:
     ```
     [idle] --(timer_expired)--> [patrol] --(player_in_range)--> [chase]
       ^                                                           |
       |___________________(player_out_of_range)___________________|
     ```
   - Validation status.
   - File paths created.
   - Suggested next steps (e.g., "Connect the AI script to your NPC node/prefab.").
