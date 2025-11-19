"""
Graph type templates for synthetic generation.
Each type includes patterns and constraints for realistic generation.
"""

GRAPH_TYPES = {
    "finite_state_machine": {
        "description": "State machines with transitions and events",
        "patterns": [
            "Session lifecycle (login, active, idle, logout)",
            "Network protocol states (connecting, connected, disconnecting)",
            "Game states (menu, playing, paused, game_over)",
            "Order processing (pending, processing, shipped, delivered)",
            "Payment flow (initiated, authorized, captured, failed)"
        ],
        "constraints": {
            "min_states": 3,
            "max_states": 8,
            "has_start_state": True,
            "has_end_states": True,
            "labeled_transitions": True
        }
    },
    
    "data_structure": {
        "description": "Binary trees, linked lists, graphs",
        "patterns": [
            "Binary search tree with values",
            "Linked list traversal",
            "Hash table with chaining",
            "Heap structure",
            "Trie for string storage"
        ],
        "constraints": {
            "min_nodes": 4,
            "max_nodes": 12,
            "hierarchical": True,
            "node_labels": "values"
        }
    },
    
    "workflow": {
        "description": "Business processes and sequential flows",
        "patterns": [
            "Document approval workflow",
            "User registration process",
            "Bug triage and resolution",
            "CI/CD pipeline stages",
            "Customer onboarding"
        ],
        "constraints": {
            "min_steps": 4,
            "max_steps": 10,
            "has_decision_points": True,
            "has_parallel_paths": False,
            "sequential_flow": True
        }
    },
    
    "architecture": {
        "description": "System architecture and component relationships",
        "patterns": [
            "Microservices architecture",
            "Layered application (presentation, business, data)",
            "Client-server topology",
            "Event-driven architecture",
            "Database replication setup"
        ],
        "constraints": {
            "min_components": 4,
            "max_components": 12,
            "show_connections": True,
            "undirected": False
        }
    },
    
    "automaton": {
        "description": "DFA, NFA for formal language recognition",
        "patterns": [
            "Recognize strings ending in '01'",
            "Accept even number of 'a's",
            "Binary number divisible by 3",
            "Strings with alternating symbols",
            "Palindrome recognizer"
        ],
        "constraints": {
            "min_states": 2,
            "max_states": 6,
            "alphabet_size": 2,
            "has_accept_states": True,
            "formal_notation": True
        }
    },
    
    "dependency_graph": {
        "description": "Package dependencies, build order, prerequisites",
        "patterns": [
            "Software package dependencies",
            "Course prerequisites",
            "Task dependencies in project",
            "Build system targets",
            "Module import relationships"
        ],
        "constraints": {
            "min_nodes": 5,
            "max_nodes": 15,
            "acyclic": True,
            "directed": True
        }
    },
    
    "class_diagram": {
        "description": "Object-oriented relationships",
        "patterns": [
            "Inheritance hierarchy",
            "Composition relationships",
            "Interface implementation",
            "Design pattern structure (Factory, Observer, etc)",
            "Domain model"
        ],
        "constraints": {
            "min_classes": 3,
            "max_classes": 8,
            "show_relationship_types": True,
            "labeled_edges": True
        }
    },
    
    "network_topology": {
        "description": "Network and communication structures",
        "patterns": [
            "Star network topology",
            "Ring topology",
            "Mesh network",
            "Client-server connections",
            "Peer-to-peer network"
        ],
        "constraints": {
            "min_nodes": 4,
            "max_nodes": 10,
            "undirected": True,
            "show_node_types": True
        }
    },
    
    "decision_tree": {
        "description": "Decision making and classification trees",
        "patterns": [
            "Animal classification",
            "Loan approval decision",
            "Medical diagnosis tree",
            "Product recommendation",
            "Troubleshooting flowchart"
        ],
        "constraints": {
            "min_depth": 2,
            "max_depth": 4,
            "binary_splits": True,
            "leaf_labels": "decisions",
            "hierarchical": True
        }
    }
}

def get_prompt_for_type(graph_type, pattern):
    """Generate a prompt for synthetic generation of a specific graph type."""
    if graph_type not in GRAPH_TYPES:
        raise ValueError(f"Unknown graph type: {graph_type}")
    
    info = GRAPH_TYPES[graph_type]
    
    prompt = f"""Generate a DOT format graph for: {pattern}

Graph Type: {graph_type}
Description: {info['description']}

Requirements:
"""
    
    for constraint, value in info['constraints'].items():
        prompt += f"- {constraint}: {value}\n"
    
    prompt += """
Output only the DOT format code, starting with 'digraph' or 'graph'.
Use clear node and edge labels.
Make it realistic and meaningful.
"""
    
    return prompt
