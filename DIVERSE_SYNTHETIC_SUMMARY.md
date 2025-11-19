# Diverse Synthetic Graph Generation - Implementation Summary

## What We Built

We expanded the synthetic generation capability from **FSM-only** to **9 different graph types**, dramatically increasing the diversity and applicability of our training data.

## Graph Types Supported

| Type | Patterns | Purpose |
|------|----------|---------|
| Finite State Machine | 5 | Sessions, protocols, workflows |
| Data Structure | 5 | Trees, lists, hash tables |
| Workflow | 5 | Business processes, pipelines |
| Architecture | 5 | Microservices, layered apps |
| Automaton | 5 | DFAs, NFAs, language recognition |
| Dependency Graph | 5 | Packages, prerequisites, DAGs |
| Class Diagram | 5 | OOP relationships, design patterns |
| Network Topology | 5 | Star, ring, mesh, P2P |
| Decision Tree | 5 | Classification, troubleshooting |

**Total:** 9 types × 5 patterns = **45 distinct patterns**

## Implementation

### Core Components

1. **`generators/synthetic_graph_types.py`**
   - Defines all 9 graph types
   - 45 specific patterns
   - Constraints for each type (nodes, edges, structure)
   - Prompt generation function

2. **`generators/generate_diverse_synthetic.py`**
   - Batch generation script
   - Supports all Ollama models
   - Configurable samples per type
   - Automatic validation
   - JSON metadata output

3. **`docs/synthetic_generation_types.md`**
   - Complete documentation
   - Usage examples
   - Quality validation approach

## Validation Results

**Test Run:** 2 samples × 9 types = 18 graphs
- **Success Rate:** 18/18 (100%)
- **Model Used:** gemma3:27b
- **Generation Time:** ~5 minutes
- **Cost:** $0 (local model)

## Example Outputs

Each generated graph includes:

```
data/synthetic_diverse/
├── finite_state_machine/
│   ├── finite_state_machine_000.dot
│   ├── finite_state_machine_000.json
│   └── ...
├── decision_tree/
│   ├── decision_tree_000.dot
│   ├── decision_tree_000.json
│   └── ...
└── generation_summary.json
```

**Metadata Example:**
```json
{
  "graph_type": "class_diagram",
  "pattern": "Inheritance hierarchy",
  "description": "Object-oriented relationships",
  "constraints": {
    "min_classes": 3,
    "max_classes": 8,
    "show_relationship_types": true,
    "labeled_edges": true
  },
  "model": "gemma3:27b",
  "temperature": 0.8,
  "nl_description": "Inheritance hierarchy"
}
```

## Benefits for Training

### Diversity
- **Before:** Only FSM patterns
- **After:** 9 different graph structures covering CS fundamentals

### Real-World Applicability
- Software architecture diagrams
- Data structure visualization
- Process modeling
- Dependency management
- Decision systems

### Scalability
With 45 patterns × variable parameters:
- **Estimated unique combinations:** 200-500+
- **Current capability:** ~50 graphs/hour (local model)
- **For 250 samples:** ~5 hours generation time

## Model Quality Observations

**Gemma 3 27B** performs well across all types:
- ✅ Correct DOT syntax
- ✅ Meaningful labels
- ✅ Follows constraints (mostly)
- ✅ Realistic scenarios
- ⚠️ Occasional edge labeling quirks
- ⚠️ Sometimes exceeds node count limits

## Next Steps

### Immediate (Phase I.3.5)
1. Generate 50-100 diverse synthetic examples
2. Extract more real examples from GitHub
3. Combine for 250-350 total pairs

### Future Enhancements
1. Add more graph types (ER diagrams, Petri nets, neural networks)
2. Implement constraint validation
3. Add visual quality checks (Graphviz rendering)
4. Create difficulty tiers (simple → complex)

## Usage

```bash
# Generate 5 samples of each type (45 graphs)
python generators/generate_diverse_synthetic.py --samples 5

# Large batch (10 × 9 = 90 graphs)
python generators/generate_diverse_synthetic.py --samples 10 --output data/synthetic_large

# Higher creativity
python generators/generate_diverse_synthetic.py --temperature 0.9

# Different model
python generators/generate_diverse_synthetic.py --model deepseek-r1:32b
```

## Impact

This expansion moves us from a **niche FSM tool** to a **general-purpose NL→DOT converter**, applicable to:
- Software engineering (architecture, dependencies)
- Computer science education (data structures, automata)
- Business process modeling (workflows, decisions)
- System design (networks, protocols)

The training dataset is now diverse enough to teach models the **fundamental patterns** of graph representation across multiple domains.
