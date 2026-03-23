"""
Luminous Verify — Validation suite for game logic and project structure.

Validates:
  - FSM JSON files for dead-end states, missing initial states, and orphan states.
  - Behavior Tree JSON files for structural integrity.
  - Project directory structures against the Luminous standard.

Usage:
  python luminous_verify.py --type fsm <path_to_json>
  python luminous_verify.py --type bt <path_to_json>
  python luminous_verify.py --type dir <path_to_project>
"""

import sys
import json
import os
import argparse


# --- ANSI Colors --------------------------------------------------------------

class Color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def success(msg):
    print(f"{Color.GREEN}[OK] {msg}{Color.RESET}")


def warning(msg):
    print(f"{Color.YELLOW}[WARN] {msg}{Color.RESET}")


def error(msg):
    print(f"{Color.RED}[ERR] {msg}{Color.RESET}")


def info(msg):
    print(f"{Color.CYAN}[INFO] {msg}{Color.RESET}")


# --- FSM Validator ------------------------------------------------------------

def verify_fsm(data):
    """
    Validates a Finite State Machine JSON structure.

    Checks performed:
      1. States list is non-empty.
      2. An initial_state is defined and exists in states.
      3. No dead-end states (states with no outgoing transition).
      4. No orphan states (states unreachable from the initial state).
      5. All transition targets reference valid states.

    Returns:
      (bool, list[str]) — (passed, list of messages)
    """
    messages = []
    passed = True

    # --- Check states exist ---
    states = data.get("states", [])
    if not states:
        return False, ["Validation Failed: No states defined."]

    state_names = [s["name"] if isinstance(s, dict) else s for s in states]
    state_set = set(state_names)

    messages.append(f"Found {len(state_names)} state(s): {', '.join(state_names)}")

    # --- Check initial state ---
    initial = data.get("initial_state")
    if initial and initial not in state_set:
        messages.append(f"Error: initial_state '{initial}' is not in the states list.")
        passed = False
    elif initial:
        messages.append(f"Initial state: '{initial}'")
    else:
        messages.append("Warning: No initial_state defined.")

    # --- Check transitions ---
    transitions = data.get("transitions", [])
    if not transitions:
        if len(state_names) > 1:
            messages.append("Error: Multiple states defined but no transitions.")
            passed = False
        else:
            messages.append("Single state with no transitions — OK.")
            return passed, messages

    # Build adjacency
    exit_sources = set()
    reachable_targets = set()

    for t in transitions:
        t_from = t.get("from")
        t_to = t.get("to")

        # Validate references
        if t_from not in state_set:
            messages.append(f"Error: Transition references unknown source state '{t_from}'.")
            passed = False
        if t_to not in state_set:
            messages.append(f"Error: Transition references unknown target state '{t_to}'.")
            passed = False

        exit_sources.add(t_from)
        reachable_targets.add(t_to)

    # --- Dead-end detection ---
    for state in state_names:
        if state not in exit_sources and len(state_names) > 1:
            messages.append(f"Logic Error: State '{state}' is a dead-end (no outgoing transitions).")
            passed = False

    # --- Orphan detection (unreachable from initial or any transition target) ---
    if initial:
        reachable = {initial} | reachable_targets
        for state in state_names:
            if state not in reachable and state != initial:
                messages.append(f"Warning: State '{state}' may be unreachable (orphan).")

    if passed:
        messages.append(f"Success: Validated {len(states)} states, {len(transitions)} transitions.")

    return passed, messages


# --- Behavior Tree Validator --------------------------------------------------

def verify_behavior_tree(data):
    """
    Validates a Behavior Tree JSON structure.

    Checks performed:
      1. Root node exists.
      2. Composite nodes (selector, sequence) have children.
      3. All nodes have a valid type.
      4. Action and condition nodes are leaf nodes (no children).

    Returns:
      (bool, list[str]) — (passed, list of messages)
    """
    messages = []
    passed = True

    root = data.get("root")
    if not root:
        return False, ["Validation Failed: No root node defined."]

    valid_types = {"selector", "sequence", "action", "condition", "decorator", "inverter", "repeater"}
    node_count = {"total": 0, "actions": 0, "conditions": 0, "composites": 0}

    def validate_node(node, depth=0):
        nonlocal passed
        node_count["total"] += 1
        prefix = "  " * depth

        node_type = node.get("type")
        node_name = node.get("name", "<unnamed>")

        if not node_type:
            messages.append(f"{prefix}Error: Node '{node_name}' has no type.")
            passed = False
            return

        if node_type not in valid_types:
            messages.append(f"{prefix}Error: Node '{node_name}' has unknown type '{node_type}'.")
            passed = False
            return

        children = node.get("children", [])

        if node_type in ("selector", "sequence"):
            node_count["composites"] += 1
            if not children:
                messages.append(f"{prefix}Error: Composite node '{node_name}' ({node_type}) has no children.")
                passed = False
            for child in children:
                validate_node(child, depth + 1)

        elif node_type in ("decorator", "inverter", "repeater"):
            child = node.get("child")
            if not child and not children:
                messages.append(f"{prefix}Error: Decorator node '{node_name}' has no child.")
                passed = False
            elif child:
                validate_node(child, depth + 1)
            elif children:
                for c in children:
                    validate_node(c, depth + 1)

        elif node_type == "action":
            node_count["actions"] += 1
            if children:
                messages.append(f"{prefix}Warning: Action node '{node_name}' should not have children.")

        elif node_type == "condition":
            node_count["conditions"] += 1
            if children:
                messages.append(f"{prefix}Warning: Condition node '{node_name}' should not have children.")

    validate_node(root)

    messages.append(
        f"Tree stats: {node_count['total']} nodes, "
        f"{node_count['composites']} composites, "
        f"{node_count['actions']} actions, "
        f"{node_count['conditions']} conditions."
    )

    if passed:
        messages.append("Success: Behavior tree is structurally valid.")

    return passed, messages


# --- Directory Validator ------------------------------------------------------

def verify_structure(path):
    """
    Validates a project directory against the Luminous standard structure.

    Checks for the presence of recommended top-level directories.

    Returns:
      (bool, list[str]) — (passed, list of messages)
    """
    messages = []

    if not os.path.isdir(path):
        return False, [f"Error: Path '{path}' is not a valid directory."]

    required = ["assets", "scripts", "src", "docs"]
    optional = ["tests", "scenes", "prefabs"]

    found_required = []
    missing_required = []
    found_optional = []

    for d in required:
        if os.path.isdir(os.path.join(path, d)):
            found_required.append(d)
        # Also check capitalized variants (Unity convention)
        elif os.path.isdir(os.path.join(path, d.capitalize())):
            found_required.append(d.capitalize())
        else:
            missing_required.append(d)

    for d in optional:
        if os.path.isdir(os.path.join(path, d)):
            found_optional.append(d)
        elif os.path.isdir(os.path.join(path, d.capitalize())):
            found_optional.append(d.capitalize())

    messages.append(f"Structure Check: {len(found_required)}/{len(required)} standard directories found.")

    if found_required:
        messages.append(f"  Found: {', '.join(found_required)}")
    if missing_required:
        messages.append(f"  Missing: {', '.join(missing_required)}")
    if found_optional:
        messages.append(f"  Optional found: {', '.join(found_optional)}")

    passed = len(found_required) >= 2  # At least 2 of 4 standard dirs

    if passed:
        messages.append("Structure is acceptable.")
    else:
        messages.append("Warning: Project structure may be incomplete.")

    return passed, messages


# --- Main ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Luminous Verify — Validate game logic and project structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python luminous_verify.py --type fsm npc_guard_ai.json
  python luminous_verify.py --type bt boss_ai.json
  python luminous_verify.py --type dir ./my-game-project
        """,
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["fsm", "bt", "dir"],
        help="Validation type: fsm (state machine), bt (behavior tree), or dir (directory structure).",
    )
    parser.add_argument(
        "path",
        help="Path to the JSON file or project directory to validate.",
    )

    args = parser.parse_args()

    print(f"\n{Color.BOLD}{'=' * 50}{Color.RESET}")
    print(f"{Color.BOLD}  Luminous Verify{Color.RESET}")
    print(f"{Color.BOLD}{'=' * 50}{Color.RESET}\n")

    if args.type == "fsm":
        info(f"Validating FSM: {args.path}")
        try:
            with open(args.path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            error(f"File not found: {args.path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            error(f"Invalid JSON: {e}")
            sys.exit(1)

        passed, messages = verify_fsm(data)

    elif args.type == "bt":
        info(f"Validating Behavior Tree: {args.path}")
        try:
            with open(args.path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            error(f"File not found: {args.path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            error(f"Invalid JSON: {e}")
            sys.exit(1)

        passed, messages = verify_behavior_tree(data)

    elif args.type == "dir":
        info(f"Validating directory structure: {args.path}")
        passed, messages = verify_structure(args.path)

    else:
        error(f"Unknown type: {args.type}")
        sys.exit(1)

    # Print all messages
    print()
    for msg in messages:
        if "Error" in msg or "Failed" in msg:
            error(msg)
        elif "Warning" in msg:
            warning(msg)
        elif "Success" in msg:
            success(msg)
        else:
            info(msg)

    print(f"\n{Color.BOLD}{'-' * 50}{Color.RESET}")
    if passed:
        success("Validation PASSED")
    else:
        error("Validation FAILED")
    print()

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()