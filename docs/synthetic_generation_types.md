# Synthetic Graph Generation - Supported Types

This document describes the graph types we can generate synthetically using LLMs.

## Overview

We've expanded beyond simple FSMs to support 9 different graph types, each with multiple patterns and constraints. This diversity helps create a robust training dataset for NL→DOT conversion.

## Supported Graph Types

### 1. Finite State Machine
**Description:** State machines with transitions and events

**Patterns:**
- Session lifecycle (login, active, idle, logout)
- Network protocol states (connecting, connected, disconnecting)
- Game states (menu, playing, paused, game_over)
- Order processing (pending, processing, shipped, delivered)
- Payment flow (initiated, authorized, captured, failed)

**Constraints:**
- 3-8 states
- Start state required
- End states required
- Labeled transitions

### 2. Data Structure
**Description:** Binary trees, linked lists, graphs

**Patterns:**
- Binary search tree with values
- Linked list traversal
- Hash table with chaining
- Heap structure
- Trie for string storage

**Constraints:**
- 4-12 nodes
- Hierarchical structure
- Node labels show values

### 3. Workflow
**Description:** Business processes and sequential flows

**Patterns:**
- Document approval workflow
- User registration process
- Bug triage and resolution
- CI/CD pipeline stages
- Customer onboarding

**Constraints:**
- 4-10 steps
- Decision points
- Sequential flow
- No parallel paths (for simplicity)

### 4. Architecture
**Description:** System architecture and component relationships

**Patterns:**
- Microservices architecture
- Layered application (presentation, business, data)
- Client-server topology
- Event-driven architecture
- Database replication setup

**Constraints:**
- 4-12 components
- Show connections
- Directed graphs

### 5. Automaton
**Description:** DFA, NFA for formal language recognition

**Patterns:**
- Recognize strings ending in '01'
- Accept even number of 'a's
- Binary number divisible by 3
- Strings with alternating symbols
- Palindrome recognizer

**Constraints:**
- 2-6 states
- Alphabet size: 2
- Accept states required
- Formal notation

### 6. Dependency Graph
**Description:** Package dependencies, build order, prerequisites

**Patterns:**
- Software package dependencies
- Course prerequisites
- Task dependencies in project
- Build system targets
- Module import relationships

**Constraints:**
- 5-15 nodes
- Acyclic (DAG)
- Directed

### 7. Class Diagram
**Description:** Object-oriented relationships

**Patterns:**
- Inheritance hierarchy
- Composition relationships
- Interface implementation
- Design pattern structure (Factory, Observer, etc)
- Domain model

**Constraints:**
- 3-8 classes
- Show relationship types (extends, implements, uses)
- Labeled edges

### 8. Network Topology
**Description:** Network and communication structures

**Patterns:**
- Star network topology
- Ring topology
- Mesh network
- Client-server connections
- Peer-to-peer network

**Constraints:**
- 4-10 nodes
- Undirected
- Show node types

### 9. Decision Tree
**Description:** Decision making and classification trees

**Patterns:**
- Animal classification
- Loan approval decision
- Medical diagnosis tree
- Product recommendation
- Troubleshooting flowchart

**Constraints:**
- Depth: 2-4 levels
- Binary splits
- Leaf nodes are decisions
- Hierarchical

## Generation Statistics

**Total Patterns:** 45
**Graph Types:** 9
**Potential Combinations:** ~200+ (with variations)

## Usage

```bash
# Generate 5 samples of each type
python generators/generate_diverse_synthetic.py --samples 5

# Use specific model
python generators/generate_diverse_synthetic.py --model gemma3:27b --samples 10

# Control creativity
python generators/generate_diverse_synthetic.py --temperature 0.9 --samples 3
```

## Quality Validation

Each generated graph includes:
1. **.dot file** - The DOT format graph
2. **.json metadata** - Graph type, pattern, constraints, NL description
3. **Format validation** - Checks that output starts with `digraph` or `graph`

## Future Expansions

Potential additional types:
- **Entity-Relationship Diagrams** - Database schemas
- **Petri Nets** - Concurrent systems
- **Neural Network Architectures** - ML model structures
- **Chemical Structures** - Molecular graphs
- **Family Trees** - Genealogy
- **Timeline Diagrams** - Historical events
