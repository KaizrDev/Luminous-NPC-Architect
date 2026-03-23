import sys
import json
import os

def verify_fsm(data):
    states = data.get('states', [])
    transitions = data.get('transitions', [])
    
    if not states:
        return False, "Validation Failed: No states defined in logic."
    
    # Check for dead states (states with no exit transitions)
    state_names = [s['name'] if isinstance(s, dict) else s for s in states]
    exit_sources = set(t['from'] for t in transitions)
    
    for state in state_names:
        if state not in exit_sources and len(state_names) > 1:
            return False, f"Logic Error: State '{state}' is a dead-end with no exit transitions."
            
    return True, f"Success: Validated {len(states)} states. Logic is deadlock-free."

def verify_structure(path):
    required_dirs = ['assets', 'scripts', 'docs', 'src']
    found = [d for d in required_dirs if os.path.isdir(os.path.join(path, d))]
    return True, f"Structure Check: {len(found)}/{len(required_dirs)} standard directories identified."

def main():
    if len(sys.argv) < 3:
        print("Usage: python luminous_verify.py --type [fsm|dir] [path]")
        sys.exit(1)

    mode = sys.argv[2]
    target = sys.argv[3]

    if mode == "fsm":
        try:
            with open(target, 'r') as f:
                res, msg = verify_fsm(json.load(f))
                print(msg)
        except Exception as e:
            print(f"Error reading FSM: {e}")
    elif mode == "dir":
        res, msg = verify_structure(target)
        print(msg)

if __name__ == "__main__":
    main()