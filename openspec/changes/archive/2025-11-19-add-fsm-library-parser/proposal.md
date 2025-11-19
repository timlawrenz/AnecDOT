# Change: Add FSM Library Parser for Logic Stream Data Collection

## Why

The Documentation Stream provides foundational DOT syntax examples, but lacks real-world code-to-graph abstraction patterns. To teach models how to translate stateful logic into graph representations, we need training pairs extracted from production FSM libraries. This implements Phase I.2 of the roadmap: building the Logic Stream pipeline to reverse-engineer DOT graphs from existing state machine code.

Without this capability, the dataset will be limited to syntax patterns and synthetic examples, missing the critical dimension of extracting graph structure from imperative code.

## What Changes

- Add static analysis tools to extract FSM class definitions from Python and Ruby codebases
- Implement dynamic execution harness to safely run `.to_dot()` methods from FSM libraries
- Create JSONL output pipeline following the established schema with `task_type: CODE_TO_DOT`
- Add validation layer to verify extracted DOT syntax using Graphviz compiler
- Provide CLI interface consistent with existing scrapers (both interactive TUI and command-line)

**Target Libraries (Initial Support):**
- Python: `python-statemachine`, `transitions`
- Ruby: `aasm` (optional, lower priority)

## Impact

**New Capability:**
- `fsm-parser` - Static analysis + dynamic DOT extraction from FSM libraries

**Affected Code:**
- `parsers/` - New directory for FSM extraction logic
- `data/` - New `logic-stream.jsonl` output file
- `common/` - May extend shared validation utilities
- `requirements.txt` - Add `tree-sitter-python`, `astroid`, or similar AST tools

**Data Pipeline Impact:**
- Adds second major data source (complements Documentation Stream)
- Expected yield: 100-500 training examples from target libraries
- Enables CODE_TO_DOT task type in training dataset

**Risk Assessment:**
- **Dynamic execution**: Requires sandboxing to prevent arbitrary code execution
- **Library diversity**: Different FSM libraries use different `.to_dot()` signatures
- **Dependency management**: Need isolated environments for each analyzed library
- **License compliance**: Must verify all source repositories are OSI-approved licenses
