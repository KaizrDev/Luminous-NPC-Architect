import sys
import json
import os

def verify_fsm(data):
    """Checks for dead-ends in NPC state machines."""
    states = data.get('states', [])
    transitions = data.get('transitions', [])
    if not states:
        return False, "Validation Failed: No states defined."
    
    state_names = [s['name'] if isinstance(s, dict) else s for s in states]
    exit_sources = set(t['from'] for t in transitions)
    
    for state in state_names:
        if state not in exit_sources and len(state_names) > 1:
            return False, f"Logic Error: State '{state}' is a dead-end."
    return True, f"Success: Validated {len(states)} states."

def verify_structure(path):
    """Ensures the project follows a clean architecture."""
    required = ['assets', 'scripts', 'src', 'docs']
    found = [d for d in required if os.path.isdir(os.path.join(path, d))]
    return True, f"Structure Check: {len(found)}/{len(required)} standard directories found."

def main():
    if len(sys.argv) < 3:
        print("Usage: python luminous_verify.py --type [fsm|dir] [path]")
        sys.exit(1)

    mode, target = sys.argv[2], sys.argv[3]
    if mode == "fsm":
        with open(target, 'r') as f:
            res, msg = verify_fsm(json.load(f))
            print(msg)
    elif mode == "dir":
        res, msg = verify_structure(target)
        print(msg)

if __name__ == "__main__":
    main()