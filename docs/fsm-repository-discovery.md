# FSM Repository Discovery Summary

**Date**: 2025-11-19  
**Goal**: Find FSM repositories to expand training dataset

## Search Results

Searched GitHub for Python FSM libraries with 50+ stars and found **16 candidates**.

---

## Top Priority Repositories

### 1. caleb531/automata ⭐ 392 🏆 **HIGHEST PRIORITY**

**Why it's valuable:**
- Academic library for DFA, NFA, PDA, Turing Machines
- Has `show_diagram()` method using pygraphviz
- Well-documented test suite with examples
- Clear natural language descriptions

**Example from test_dfa.py:**
```python
# This DFA accepts all words which do not contain two
# consecutive occurrences of 1
no_consecutive_11_dfa = DFA(
    states={"p0", "p1", "p2"},
    input_symbols={"0", "1"},
    transitions={
        "p0": {"0": "p0", "1": "p1"},
        "p1": {"0": "p0", "1": "p2"},
        "p2": {"0": "p2", "1": "p2"},
    },
    initial_state="p0",
    final_states={"p0", "p1"},
)
```

**Extraction potential:**
- 20+ DFA examples in test_dfa.py alone
- NFA, PDA, Turing Machine examples
- Each has natural language description
- Can call `.show_diagram()` to get DOT

**License**: MIT ✅

**Status**: Cloned to /tmp/automata

---

### 2. pgularski/pysm ⭐ 76

**Why it's valuable:**
- Hierarchical State Machine (HSM) support
- Has `examples/` folder
- Different pattern from our current dataset
- MicroPython support (embedded systems domain)

**Extraction potential:**
- Examples folder to inspect
- Hierarchical states (NEW pattern!)
- Embedded/robotics domain

**License**: MIT ✅

**Status**: To be cloned

---

### 3. oozie/python-fsm ⭐ 21

**Why it's valuable:**
- Description mentions "pygraphviz hook"
- Focused specifically on visualization
- Simple, might have clean examples

**Extraction potential:**
- Small codebase, easy to extract all examples
- Explicitly designed for graph generation

**License**: MIT ✅

**Status**: To be cloned

---

## Secondary Candidates

### 4. alysivji/finite-state-machine ⭐ 114

- Decorator-based pattern (different from current)
- Topics include "state-diagram"
- Modern Python (type hints)

**Extraction**: Moderate - need to check if has DOT export

---

### 5. viewflow/django-fsm ⭐ 2,344

- Django-specific workflows
- Real-world business logic patterns
- Topics: "state-machine-diagram"
- **Status**: Archived (still usable)

**Extraction**: High value - real-world patterns, but Django-specific

---

### 6. uleroboticsgroup/yasmin ⭐ 220

- ROS2 state machine
- Robotics domain (unique!)
- Active development
- C++ and Python

**Extraction**: High value - robotics patterns, but ROS2-specific

---

## Pattern Analysis

### New Patterns We Could Learn

From **caleb531/automata**:
- DFA/NFA patterns (formal automata theory)
- Input alphabet and transitions
- Accept/reject states
- Regular language recognition

From **pgularski/pysm**:
- Hierarchical state machines
- Nested states
- State composition

From **viewflow/django-fsm**:
- Business workflow patterns
- Permission-based transitions
- Real-world domain models

From **yasmin**:
- Robotics behaviors
- ROS2 service calls
- Sensor-driven state changes

---

## Extraction Strategy

### Phase 1: Quick Wins (1-2 hours)

1. **caleb531/automata** - Extract DFA/NFA examples
   - Inspect test_dfa.py, test_nfa.py
   - Run show_diagram() on each example
   - Extract 20-30 pairs

2. **oozie/python-fsm** - Check pygraphviz examples
   - Small codebase, quick extraction
   - Estimate: 5-10 pairs

**Estimated Total**: 25-40 new pairs

---

### Phase 2: Medium Effort (2-4 hours)

3. **pgularski/pysm** - Hierarchical examples
   - Inspect examples/ folder
   - Check if has visualization
   - Estimate: 10-15 pairs

4. **alysivji/finite-state-machine**
   - Check for visualization support
   - Estimate: 5-10 pairs if supported

**Estimated Total**: 15-25 new pairs

---

### Phase 3: High Effort (4-8 hours)

5. **viewflow/django-fsm** - Real-world workflows
   - Domain-specific, need Django knowledge
   - Would need to extract from docs/examples
   - Estimate: 10-20 pairs

6. **yasmin** - Robotics patterns
   - ROS2-specific, need domain knowledge
   - Estimate: 5-15 pairs

**Estimated Total**: 15-35 new pairs

---

## Recommended Immediate Action

### Option A: Extract from automata NOW ✅ **RECOMMENDED**

**Time**: 1-2 hours  
**Yield**: 25-40 pairs  
**Quality**: High (academic, well-documented)

**Steps**:
1. Enhance fsm_extractor to support automata library
2. Run on test_dfa.py, test_nfa.py, test_pda.py
3. Extract code + call show_diagram() for DOT
4. Pair with docstring descriptions

**Benefits**:
- Immediate high-quality pairs
- New patterns (DFA, NFA formal automata)
- Clean code examples
- MIT licensed

---

### Option B: Clone All Top 3, Then Decide

**Time**: 30 minutes + analysis  
**Yield**: TBD  

Clone pysm and python-fsm, inspect all three, then pick best targets.

---

### Option C: Generate Synthetic First

Based on what we learned from automata:
- DFA patterns (binary alphabet, accept states)
- NFA patterns (non-deterministic transitions)
- New prompts for synthetic generation

**Time**: 1 hour  
**Yield**: 20-30 synthetic pairs  

---

## Patterns for Synthetic Generation

### New Domains from Research

1. **Formal Automata**:
   - "A DFA that accepts binary strings with even number of 1s"
   - "An NFA that recognizes strings ending in '01'"
   - "A DFA for validating email format"

2. **Hierarchical States**:
   - "A robot controller with hierarchical behaviors: move (forward, backward), turn (left, right), stop"
   - "A game AI with composite states: combat (melee, ranged), navigation, idle"

3. **Business Workflows**:
   - "A loan approval workflow with states: submitted, under_review, approved, rejected, pending_documents"
   - "An order fulfillment FSM: received, picked, packed, shipped, delivered, returned"

4. **Protocol States**:
   - "WebSocket connection FSM: connecting, open, closing, closed"
   - "OAuth flow: unauthorized, authorizing, authorized, token_refresh, revoked"

---

## Recommendation

**Start with caleb531/automata**:
1. It's already cloned
2. Has clear examples with descriptions
3. High-quality, well-tested code
4. Can extract 25-40 pairs in 1-2 hours
5. Introduces formal automata patterns

**Then**:
- Use new patterns to enhance synthetic generation
- Move to pysm for hierarchical patterns
- Reassess after reaching 100-120 total pairs

---

## Expected Dataset Growth

**Current**: 68 pairs (58 real + 10 synthetic)

**After automata extraction**: 93-108 pairs (40% growth!)

**After Phase 1+2**: 108-133 pairs (50-75 more)

**Target**: 250-350 pairs

**Gap remaining**: 117-242 pairs

---

## Next Decision Point

Do you want to:

A. Start extracting from caleb531/automata now
B. Clone and inspect all top 3 first
C. Create new synthetic prompts based on patterns learned
D. Something else

**Recommendation**: A - Start extracting from automata

## Extraction Results

### ✅ Completed Extractions

1. **caleb531/automata** - 18 DFA pairs ✓
   - Extracted from test_dfa.py
   - All have natural language descriptions
   - Location: `data/raw/automata_extraction/`

2. **oozie/python-fsm** - 3 pairs ✓
   - TCP/IP protocol state machine
   - Parking meter (Moore machine)
   - Binary adder (Mealy machine)
   - Location: `data/raw/python_fsm_extraction/`

**Total extracted this session: 21 pairs**
**Dataset size: 68 → 89 pairs (+31%)**
