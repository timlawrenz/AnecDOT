# Design: Attribute Documentation Scraper

## Problem Analysis

### Feasibility Assessment

**Prototype results (3 attribute pages tested):**
- ✅ All pages have extractable DOT examples
- ✅ Attribute names are clearly identifiable
- ⚠️ Descriptions vary in quality (some technical, some verbose)
- ✅ Examples are valid DOT code

**Generated instruction quality:**
```
"Demonstrate the 'cluster' attribute usage in Graphviz. Subgraph clusters 
are rendered differently, e.g. dot renders a box around subgraph clusters..."
```
→ **Verdict: Acceptable** for attribute-focused training

### Comparison with Gallery Examples

| Aspect | Gallery | Attribute Docs |
|--------|---------|----------------|
| Instruction clarity | High (curated) | Medium (heuristic) |
| DOT complexity | Varied | Focused on specific attributes |
| Training value | General usage | Fine-grained control |
| Instruction confidence | 95% | 75% |
| Quantity | ~50 examples | ~100+ examples |

### Decision: Proceed with Confidence Tagging

**Approach:** Implement heuristic scraper with `instruction_confidence` metadata

## Design Decisions

### Decision 1: Two-Tier Instruction Generation

**Rationale:** Different attributes have different description quality.

**Implementation:**
- **Tier 1 (High confidence):** Attributes with clear, concise descriptions
  - Use: "Demonstrate {attr_name}. {description}"
  - Confidence: 0.8
  
- **Tier 2 (Medium confidence):** Technical/sparse descriptions
  - Use: "Show usage of the '{attr_name}' attribute in Graphviz"
  - Confidence: 0.6

**Quality filter:** Only include examples with confidence ≥ 0.6

### Decision 2: Extend Schema with Confidence Field

**Add optional field to DataRecord:**
```python
instruction_confidence: Optional[float] = None  # 0.0-1.0
```

**Usage:**
- Gallery examples: 1.0 (curated)
- FSM examples: 0.9 (code-to-DOT is clear)
- Attribute docs: 0.6-0.8 (heuristic)
- Synthetic: varies by teacher model

**Benefit:** Allows filtering/weighting during training

### Decision 3: Template-Based Instruction Generation

**Templates by context:**

1. **Attribute with clear description:**
   ```
   "Demonstrate the {attr_name} attribute. {description_first_sentence}"
   ```

2. **Attribute with examples in description:**
   ```
   "Use the {attr_name} attribute to {extracted_purpose}"
   ```

3. **Fallback:**
   ```
   "Show how to use the '{attr_name}' attribute in a Graphviz graph"
   ```

### Decision 4: Attribute Page Discovery

**Strategy:**
1. Scrape main attrs.html for links to `/docs/attrs/*/`
2. Estimated ~120 attribute pages
3. Filter pages with DOT examples
4. Expected yield: 50-80 valid examples

### Decision 5: Deduplication with Gallery

**Issue:** Some attribute pages may have examples that overlap with gallery

**Solution:** Content-hash IDs (already implemented) will catch duplicates
- If attribute example DOT matches gallery DOT → skip (duplicate)
- If slightly different → keep both (variations are valuable)

## Architecture

### Reuse from Phase I.1

```python
from validation.dot_validator import validate_dot
from validation.schema import DataRecord  # Extended with confidence
from validation.writer import JSONLWriter
from common.id_generator import generate_id
from common.metrics import ScraperMetrics
```

**New code:** ~200 LOC (attribute-specific extraction logic only)

### Scraper Flow

```
1. Fetch attrs.html
2. Extract links to /docs/attrs/*/ pages
3. For each attribute page:
   a. Extract attribute name
   b. Extract description
   c. Extract DOT example(s)
   d. Generate instruction (with confidence score)
   e. Validate DOT
   f. Write to JSONL
4. Summary statistics
```

## Open Questions

### Q1: Should we extract ALL attribute pages or filter?

**Options:**
- A. Scrape all ~120 pages → max coverage, some low-quality
- B. Filter by attribute importance → higher quality, less coverage
- C. Sample 20-30 pages, assess quality, then decide

**Recommendation:** Option A (scrape all), use confidence scores to filter later

### Q2: How to handle multiple examples per attribute?

**Observation:** Some attributes (like `color`, `label`) have multiple examples

**Solution:** Same as gallery - extract each as separate record with index suffix

### Q3: Should this be Phase I.2 or defer?

**Arguments for Phase I.2:**
- Quick to implement (reuse infrastructure)
- Adds 50-80 attribute-focused examples
- Complements gallery examples nicely

**Arguments for defer:**
- FSM parser (original Phase I.2) is code-to-DOT (different task type)
- Should collect code-based examples before more NL-to-DOT
- Attribute docs might be better done with synthetic generation

**Recommendation:** Make this **Phase I.1b** (bonus) - quick addition, doesn't block FSM parser

## Implementation Plan

### Minimal Viable Scraper (2-3 hours)

1. Copy `graphviz_gallery.py` → `attribute_docs.py`
2. Modify page discovery (attrs.html → individual attribute pages)
3. Implement instruction generation with templates
4. Add confidence scoring
5. Test on 10 pages, verify quality
6. If acceptable, run full scrape

### Schema Extension

Update `validation/schema.py`:
```python
@dataclass
class DataRecord:
    # ... existing fields ...
    instruction_confidence: Optional[float] = None
```

### Success Criteria

- ≥40 validated DOT examples extracted
- Average confidence score ≥0.7
- 100% compiler pass rate
- No duplicates with gallery examples (detected by hash)

## Risks & Mitigations

### Risk: Low instruction quality

**Mitigation:** 
- Use confidence scores
- Filter out low-confidence (<0.6) during training
- Manual spot-check sample before full run

### Risk: Overlaps with gallery

**Mitigation:**
- Content-hash deduplication (already implemented)
- Both writer and merge will catch duplicates

### Risk: Attribute descriptions too technical

**Mitigation:**
- Template-based fallbacks
- Confidence scoring marks technical ones as lower quality
- Can be filtered later or improved with GPT-4 rewriting

## Timeline

**If approved as Phase I.1b:**
- Implementation: 2-3 hours
- Testing & validation: 1 hour
- Documentation: 30 minutes
- **Total: ~4 hours**

Much faster than original Phase I.2 (FSM parser) due to infrastructure reuse.
