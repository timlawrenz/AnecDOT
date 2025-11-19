# Change: Add Attribute Documentation Scraper

## Why

The Graphviz attribute documentation (https://www.graphviz.org/doc/info/attrs.html and individual attribute pages like https://www.graphviz.org/docs/attrs/cluster/) contains DOT code examples demonstrating attribute usage. However, unlike the Gallery examples, the relationship between natural language instruction and DOT code is less direct:

- **Gallery examples** have clear titles/descriptions → well-defined instructions
- **Attribute pages** have technical definitions → requires heuristics to create instructions

This proposal explores whether we can generate high-quality training pairs from attribute documentation using heuristics, or if human curation is needed.

**Current Gap:** Phase I.1 collected 13 gallery examples. Attribute docs could add 50-100+ examples focused on specific attribute usage patterns, which are valuable for teaching the model fine-grained control.

## What Changes

**Option A: Heuristic-Based Extraction (Proposed)**
- Scrape attribute documentation pages
- Extract DOT examples with attribute definitions
- Generate synthetic instructions using templates:
  - "Demonstrate the [attribute_name] attribute"
  - "Show how to use [attribute_name] in [context]"
  - Extract attribute description as context
- Validate all DOT code with compiler
- Tag records with `source: "attribute_docs"` and `confidence: "heuristic"`

**Option B: Semi-Automated with Review (Alternative)**
- Extract examples as in Option A
- Generate candidate instructions
- Manual review/editing of instruction quality
- Higher quality but slower, doesn't scale

**Option C: Defer to Synthetic Generation (Alternative)**
- Skip attribute docs scraper
- Use GPT-4 in Phase I.3 to generate attribute-focused examples
- Avoids low-quality heuristic instructions

## Impact

**If Option A (Heuristic):**
- **New capability**: `specs/attribute-docs-scraper/`
- **New code**: `scrapers/attribute_docs.py` (~200 LOC)
- **Reuses**: All shared infrastructure from Phase I.1 (validator, schema, writer)
- **Output**: `data/attribute-docs-stream.jsonl` (estimated 50-100 records)
- **Risk**: Instruction quality may be lower than gallery examples

**Open Questions:**
1. Can we generate adequate instructions from attribute names + descriptions?
2. Should we add `instruction_confidence` field to schema for heuristic vs curated?
3. Is attribute documentation valuable enough to justify potentially lower-quality instructions?
4. Should this be Phase I.2 or deferred after FSM parser?

## Recommendation

**Investigate first, decide second:**
1. Build a prototype scraper (1-2 hours)
2. Generate 10-20 example pairs
3. Manually assess instruction quality
4. Decide: proceed with heuristics, add manual review, or skip

If instruction quality is acceptable (>80% usable), proceed as Phase I.2.  
If quality is poor (<60% usable), defer to Phase I.3 synthetic generation.
