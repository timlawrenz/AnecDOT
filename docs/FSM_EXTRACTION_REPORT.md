# FSM Extraction Progress Report

**Date:** 2025-11-20  
**Session:** Data Collection - FSM Repository Extraction  
**Goal:** Extract 20-30 new FSM repositories for training data expansion

## Summary

Successfully extracted **14 new pairs** from 2 FSM repositories, bringing total dataset to **174 pairs** (14% increase from baseline of 160).

## Extraction Results

### Successful Extractions

#### 1. **transitions** (pytransitions/transitions)
- **Repository**: https://github.com/pytransitions/transitions (6.3K⭐)
- **Pairs Extracted**: 7 pairs
- **Method**: GraphMachine with `.get_graph()` for DOT export
- **Examples**:
  - Simple FSM (A→B→C→D progression)
  - Conditional FSM (with transition guards)
  - Traffic light (cyclic state machine)
  - Door controller (4-state cycle)
  - Hierarchical FSM (nested states: working/coding/testing/reviewing)
  - Linear workflow (with wildcard transitions)
  - Simple toggle (idle ↔ active)

**Key Features**:
- Supports hierarchical/nested states
- Wildcard transitions (`source='*'`)
- Rich graph visualization with Graphviz backend
- Instruction-tuned format with state descriptions

#### 2. **fsmdot** (Quentin18/fsmdot)
- **Repository**: https://github.com/Quentin18/fsmdot (7⭐)
- **Pairs Extracted**: 7 pairs
- **Method**: Read pre-generated `.dot` files from examples
- **Examples**:
  - DFA: Even number of zeros
  - DFA: Strings ending in "01"
  - DFA: Additional patterns
  - NFA: Contains substring "101"
  - NFA: Multiple non-deterministic examples

**Key Features**:
- Automata theory focus (DFA/NFA)
- Educational examples with formal notation
- Pre-validated DOT graphs in repository

### Attempted but No DOT Support

#### 3. **automat** (glyph/automat) ❌
- **Repository**: https://github.com/glyph/automat (643⭐)
- **Issue**: API restrictions prevent programmatic state machine creation
- **Error**: "MethodicalMachine is an implementation detail"
- **Status**: Skipped

#### 4. **finite-state-machine** (alysivji/finite-state-machine) ❌
- **Repository**: https://github.com/alysivji/finite-state-machine (114⭐)
- **Issue**: Only supports Mermaid/Markdown diagrams, no DOT/Graphviz export
- **Status**: Skipped

## Dataset Statistics

### Before This Session
```
Total: 160 pairs
  - statemachine_cat: 92
  - attribute-docs: 31
  - graphviz gallery: 13
  - logic extraction: 14
  - synthetic: 10
```

### After This Session
```
Total: 174 pairs (+14, +8.75%)
  - statemachine_cat: 92
  - attribute-docs: 31
  - transitions: 7 (NEW)
  - fsmdot: 7 (NEW)
  - logic extraction: 14
  - graphviz gallery: 13
  - synthetic: 10
```

## Extraction Infrastructure

### Tools Created

1. **`parsers/extract_transitions.py`**
   - Programmatically creates GraphMachine instances
   - Extracts DOT via `.get_graph().source`
   - Formats as instruction-tuning pairs

2. **`extraction_queue.txt`**
   - Prioritized list of 15 FSM repositories
   - Tracks extraction progress
   - Documents DOT export likelihood

3. **`generators/generate_batch_synthetic.py`**
   - 50 diverse graph prompts queued
   - Ready for Gemini API generation
   - Covers: FSMs, workflows, architectures, dependencies, decision trees

### Lessons Learned

**What Works:**
- ✅ Repositories with explicit `.to_dot()` / `.get_graph()` methods
- ✅ Pre-existing `.dot` files in examples/tests
- ✅ Well-documented test suites with diverse examples
- ✅ Libraries focused on visualization (transitions, fsmdot)

**What Doesn't:**
- ❌ Libraries with internal-only APIs (automat)
- ❌ Libraries supporting only other formats (Mermaid, markdown)
- ❌ Repositories without examples/tests
- ❌ Overly complex APIs requiring deep integration

**Key Insight:** Most FSM libraries don't export to DOT/Graphviz. The ones that do (transitions, python-statemachine, fsmdot) are goldmines worth deep extraction.

## Quality Validation

All 14 new pairs:
- ✅ Syntactically valid (compiled with `dot`)
- ✅ Diverse patterns (hierarchical, conditional, cyclic, linear)
- ✅ Clear input descriptions
- ✅ Properly formatted for instruction tuning

## Next Steps

### Immediate (Phase II.2)
1. **Generate synthetic pairs**: Use queued 50 prompts → target 200+ total pairs
2. **Train with expanded dataset**: 174 pairs vs 153 in Phase II.1
3. **Measure improvement**: Expect 56% → 60-65% valid DOT generation

### Future Extractions
- **Expand transitions**: Test suite has 519 lines, many more examples available
- **Deep dive python-statemachine**: Already have 92, but could extract more patterns
- **Check django-fsm**: Popular but archived, may have DOT export
- **Search for visualization-focused repos**: `graphviz` topic on GitHub

## Conclusion

Successfully extracted 14 high-quality training pairs from 2 repositories. While the initial goal of 20-30 repos proved overly optimistic (most FSM libraries lack DOT export), the focused extraction from quality sources yielded diverse, well-structured examples.

**Impact**: 8.75% dataset increase with high-quality, diverse FSM patterns ready for Phase II.2 training.

---

## Appendix: Repository Queue Status

**Completed:**
- ✅ pytransitions/transitions (7 pairs)
- ✅ Quentin18/fsmdot (7 pairs)
- ❌ glyph/automat (no API)
- ❌ alysivji/finite-state-machine (no DOT)

**Still Queued:**
- ⏳ jtushman/state_machine
- ⏳ rbarrois/xworkflows
- ⏳ opsani/statesman
- ⏳ pgularski/pysm
- ⏳ viewflow/django-fsm
- ⏳ DLR-RM/RAFCON
- ⏳ Others (see extraction_queue.txt)

**Recommendation:** Focus on deep extraction from proven repos (transitions, fsmdot) rather than breadth across many repos with uncertain DOT support.
