# Training Data Sources

This file tracks all repositories and sources used to generate training examples.

## Repository Sources

### 1. pytransitions/transitions
- **URL**: https://github.com/pytransitions/transitions
- **Stars**: 6,309
- **License**: MIT
- **Extracted**: 2025-11-19
- **Examples Count**: 10 (code, dot) pairs
- **Description**: Lightweight FSM library with GraphMachine for DOT export
- **Patterns**: Basic state machines, hierarchical states, callbacks

### 2. fgmacedo/python-statemachine
- **URL**: https://github.com/fgmacedo/python-statemachine
- **Stars**: 1,158
- **License**: MIT
- **Extracted**: 2025-11-19
- **Examples Count**: 4 (code, dot) + 44 (nl, dot) pairs from docs
- **Description**: Python FSM with state diagrams and DSL
- **Patterns**: State machines with events, transitions, guards

### 3. caleb531/automata
- **URL**: https://github.com/caleb531/automata
- **Stars**: 392
- **License**: MIT
- **Extracted**: 2025-11-19
- **Examples Count**: 18 DFA examples
- **Description**: Academic library for DFA, NFA, PDA, Turing Machines
- **Patterns**: Formal automata theory, accept/reject states, input alphabets, binary string validation
- **Notes**: Extracted from test_dfa.py using show_diagram() method

### 4. oozie/python-fsm
- **URL**: https://github.com/oozie/python-fsm
- **Stars**: 21
- **License**: MIT
- **Extracted**: 2025-11-19
- **Examples Count**: 3 examples (TCP/IP, Parking Meter, Binary Adder)
- **Description**: Python FSM with pygraphviz hook for visualization
- **Patterns**: Protocol states (TCP/IP), Moore machines, Mealy machines, real-world systems
- **Notes**: Extracted from README examples

---

## Synthetic Sources

### 1. Ollama gemma2:27b
- **Generated**: 2025-11-19
- **Examples Count**: 10 validation pairs
- **Method**: Zero-shot prompting with scenario descriptions
- **Patterns**: Traffic lights, vending machines, authentication, game states

---

## Statistics

**Total Pairs**: 89
- Real extracted: 79
  - transitions: 10 (code, dot)
  - python-statemachine: 48 (4 code + 44 nl, dot)
  - automata: 18 (code, dot)
  - python-fsm: 3 (code, dot)
- Synthetic: 10 (nl, dot)

**By Type**:
- (code, dot): 35 pairs
- (nl, dot): 44 pairs  
- (synthetic nl, dot): 10 pairs

**Last Updated**: 2025-11-19
