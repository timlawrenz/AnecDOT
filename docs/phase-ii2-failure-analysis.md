# Phase II.2 Failure Analysis

**Date:** 2025-11-21  
**Model:** Gemma-2B fine-tuned with 273 pairs  
**Failures:** 10/27 (37.0%)  
**Successes:** 17/27 (63.0%)

---

## Failure Breakdown

### Categories
- **No DOT found:** 4 cases (14.8%)
- **Invalid syntax:** 6 cases (22.2%)

---

## No DOT Found (4 cases)

### Example #4 - Attribute demonstration
**Source:** attribute_docs  
**Issue:** Model generated node definitions without `digraph` wrapper  
**Root cause:** Training data may have snippet-only examples  
**Fix:** Ensure all training examples have complete digraph structure

### Example #16 - Python code domain
**Source:** python-statemachine example  
**Issue:** Model generated Python code instead of DOT  
**Root cause:** Input was Python code, model echoed it back  
**Fix:** Better prompt engineering or filter Python→DOT examples

### Example #17 - State-machine-cat syntax
**Source:** statemachine_cat  
**Issue:** Model did generate DOT but extraction failed  
**Root cause:** Complex nested states with HTML labels  
**Fix:** Improve extraction regex or model training on complex cases

### Example #24 - Natural language FSM
**Source:** transitions comprehensive  
**Issue:** Output truncated mid-generation  
**Root cause:** Hit token limit (1024 tokens)  
**Fix:** Increase max_tokens or train to generate more concise DOT

---

## Invalid Syntax (6 cases)

### Example #2 - NFA automaton
**Source:** fsmdot  
**Syntax error:** Line 23 near '\\'  
**Issue:** Incorrectly escaped characters in labels  
**Pattern:** `label="    \l"` (invalid escape sequence)

### Example #8 - Traffic light transitions
**Source:** python-statemachine  
**Syntax error:** Line 1 near '`'  
**Issue:** Used backticks instead of quotes  
**Pattern:** `digraph `transitions``  instead of `digraph "transitions"`

### Example #10 - Nested states
**Source:** state-machine-cat  
**Syntax error:** Line 18 near '>'  
**Issue:** Malformed HTML-like label  
**Pattern:** Unclosed or mismatched tags in label

### Example #20 - Terminal state
**Source:** state-machine-cat  
**Syntax error:** Line 9 near '"'  
**Issue:** Quote mismatch in attribute  
**Pattern:** Incorrect quote escaping

### Example #21 - Minimal graph
**Source:** statemachine_cat  
**Syntax error:** Line 2 near '.'  
**Issue:** Invalid character in graph definition  
**Pattern:** Graph nearly empty (36 chars), malformed

### Example #22 - Hierarchical states
**Source:** statemachine_cat  
**Syntax error:** Line 37 near '--'  
**Issue:** Used wrong edge operator (`--` instead of `->`)  
**Pattern:** Mixed directed/undirected graph syntax

---

## Pattern Analysis

### Common Failure Modes

1. **Quote/Escape Issues (3 cases)**
   - Wrong quote types (backticks vs quotes)
   - Incorrect escape sequences (`\l` misuse)
   - Quote mismatch

2. **HTML Label Problems (2 cases)**
   - Unclosed table tags
   - Malformed HTML-like structures
   - Complex nested labels

3. **Wrong Output Type (2 cases)**
   - Generated Python code instead of DOT
   - Generated partial/incomplete structures

4. **Edge Operator Confusion (1 case)**
   - Used `--` (undirected) in `digraph` (directed)

5. **Truncation (1-2 cases)**
   - Hit 1024 token limit
   - Incomplete graph generation

---

## Root Cause Summary

| Root Cause | Count | % of Failures |
|------------|-------|---------------|
| Syntax errors (quotes, escapes) | 3 | 30% |
| HTML label complexity | 2 | 20% |
| Wrong output type | 2 | 20% |
| Truncation/incomplete | 2 | 20% |
| Edge operator confusion | 1 | 10% |

---

## Improvement Opportunities

### Quick Wins (would fix 4-5 failures)

1. **Post-processing fixes**
   - Auto-correct backticks to quotes
   - Fix common escape sequence errors
   - Add missing closing braces
   - **Potential gain:** +2-3 valid examples (→ 70-74%)

2. **Better prompt engineering**
   - Explicitly request "valid Graphviz DOT only"
   - Add constraint: "use -> for directed edges"
   - **Potential gain:** +1-2 examples (→ 67-70%)

### Medium-term fixes (training-based)

3. **Filter/fix training data**
   - Remove Python code → DOT examples
   - Simplify HTML labels in training set
   - Add more examples with proper quote usage
   - **Potential gain:** +2-3 examples (→ 70-74%)

4. **Increase model capacity**
   - Try Qwen3-4B (4B params vs 2B)
   - Better handling of complex structures
   - **Expected:** 75-80% success rate

### Long-term improvements

5. **Multi-stage generation**
   - Stage 1: Generate abstract structure (JSON)
   - Stage 2: Convert to DOT syntax
   - Reduces syntax errors

6. **Validator in training loop**
   - Use DOT compiler feedback during training
   - Reward syntactically valid outputs

---

## Conclusions

### What the Model Learned Well
- ✅ Basic DOT structure (17/27 = 63%)
- ✅ Simple state machines
- ✅ Node and edge definitions
- ✅ Basic attributes

### What the Model Struggles With
- ⚠️ Quote/escape sequences (3 errors)
- ⚠️ Complex HTML labels (2 errors)
- ⚠️ Distinguishing Python code from DOT (2 errors)
- ⚠️ Long graph generation (1-2 truncations)

### Is 63% Good Enough?

**For assisted workflows:** YES
- 2 out of 3 examples work
- Failures are often minor (fixable with post-processing)
- Human can quickly correct syntax errors

**For fully automated:** NOT YET
- Need 90%+ for production
- Current 37% failure rate too high
- But within reach with improvements above

---

## Recommendations

**Immediate:**
1. Implement post-processing (quote fixes, brace completion)
2. Run evaluation with fixes → likely 70-74% success

**Next training run (Phase II.3):**
1. Try Qwen3-4B model (2x capacity)
2. Filter problematic training examples
3. Target: 75-80% success rate

**Future work:**
1. Multi-stage generation approach
2. Validator-guided training
3. Larger dataset (500+ pairs)
4. Target: 90%+ success rate

---

**Status:** Analysis complete  
**Key insight:** Most failures are minor syntax errors, not fundamental misunderstandings  
**Path forward:** Model capacity increase + post-processing = 75-80% achievable

