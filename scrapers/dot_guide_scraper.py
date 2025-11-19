#!/usr/bin/env python3
"""
Scraper for DOT language guide examples.
Extracts DOT diagrams with natural language descriptions from tutorial sites.
"""

from pathlib import Path
import re
import html

# Manual extraction from https://www.danieleteti.it/post/dot-language-guide-for-devs-and-analysts-en/

EXAMPLES = [
    {
        "name": "first_graph",
        "description": "First example graph showing a simple process flow with error handling",
        "dot": """digraph MyFirstGraph {
    node [shape=box, style=rounded, fillcolor=lightblue, style="rounded,filled"];
    edge [color=blue];

    Start -> Process -> End;
    Process -> Error [style=dashed, label="on failure"];
    Error -> Start [label="retry"];
}""",
        "category": "workflow"
    },
    {
        "name": "flowchart_authentication",
        "description": "Professional flowchart for authentication system showing decisions, processes, and logical flow",
        "dot": """digraph Flow {
    graph [rankdir=TB, nodesep=0.6];
    node [fontname="Arial"];

    Start   [shape=oval, style=filled, fillcolor="#C1F2C7"];
    Check   [shape=diamond, label="Valid input?"];
    Process [shape=box, style=rounded];
    Error   [shape=box, style=filled, fillcolor="#FFCCCB"];
    End     [shape=oval, style=filled, fillcolor="#D3D3D3"];

    Start -> Check;
    Check -> Process [label="yes"];
    Check -> Error [label="no"];
    Process -> End;
    Error -> Start [label="retry"];
}""",
        "category": "flowchart"
    },
    {
        "name": "state_machine_async_request",
        "description": "State machine modeling lifecycle of an asynchronous request with states: Idle, Loading, Ready, and Error",
        "dot": """digraph States {
    graph [rankdir=LR];
    node [shape=circle, fontsize=12];

    Idle -> Loading   [label="start"];
    Loading -> Ready  [label="success"];
    Loading -> Error  [label="fail"];
    Error -> Idle     [label="reset"];
    Ready -> Idle     [label="finish"];
}""",
        "category": "state_machine"
    },
    {
        "name": "dependency_graph",
        "description": "Dependency graph showing module relationships with UI, API, Service, and Database layers",
        "dot": """digraph Deps {
    graph [rankdir=LR];
    node [shape=box, style=filled, fillcolor="#F7FAFF", fontname="Inter"];
    edge [color="#555555"];

    UI -> API;
    API -> Service;
    API -> Cache [style=dashed, label="optional"];
    Service -> Database;
    Cache -> Database [style=dashed];
}""",
        "category": "architecture"
    },
    {
        "name": "layered_architecture",
        "description": "Layered architecture diagram with Presentation Layer, Business Layer, and Data Layer using clusters",
        "dot": """digraph Architecture {
    graph [rankdir=TB, ranksep=0.8, nodesep=0.6];
    node [shape=box, style=filled, fillcolor="#E8F4F8"];

    subgraph cluster_presentation {
        label="Presentation Layer";
        style=filled;
        fillcolor="#FFE5E5";
        UI; Controller;
    }

    subgraph cluster_business {
        label="Business Layer";
        style=filled;
        fillcolor="#E5FFE5";
        Service; Logic;
    }

    subgraph cluster_data {
        label="Data Layer";
        style=filled;
        fillcolor="#E5E5FF";
        Repository; Database [shape=cylinder];
    }

    UI -> Controller;
    Controller -> Service;
    Service -> Logic;
    Logic -> Repository;
    Repository -> Database;
}""",
        "category": "architecture"
    },
    {
        "name": "microservices_map",
        "description": "Microservices architecture map showing Edge Gateway, Core Services, and Data layers with protocol labels",
        "dot": """digraph Micro {
    graph [rankdir=LR, splines=true];
    node [shape=box, style=filled, fillcolor="#F0F0F0"];

    subgraph cluster_gateway {
        label="Edge";
        style=filled;
        fillcolor="#FFE5CC";
        Gateway;
    }

    subgraph cluster_services {
        label="Services";
        style=filled;
        fillcolor="#E5F2FF";
        AuthService;
        OrderService;
        PaymentService;
    }

    subgraph cluster_data {
        label="Data";
        style=filled;
        fillcolor="#E5FFE5";
        UserDB [shape=cylinder];
        OrderDB [shape=cylinder];
    }

    Gateway -> AuthService [label="HTTP"];
    Gateway -> OrderService [label="gRPC"];
    OrderService -> PaymentService [label="REST"];
    AuthService -> UserDB;
    OrderService -> OrderDB;
}""",
        "category": "microservices"
    },
    {
        "name": "tcp_state_machine",
        "description": "TCP protocol state machine with standard states: CLOSED, LISTEN, SYN_SENT, ESTABLISHED, etc.",
        "dot": """digraph TCP {
    graph [rankdir=LR];
    node [shape=circle];

    CLOSED -> LISTEN [label="passive open"];
    CLOSED -> SYN_SENT [label="active open"];
    LISTEN -> SYN_RECEIVED [label="SYN"];
    SYN_SENT -> ESTABLISHED [label="SYN+ACK"];
    SYN_RECEIVED -> ESTABLISHED [label="ACK"];
    ESTABLISHED -> FIN_WAIT_1 [label="close"];
    ESTABLISHED -> CLOSE_WAIT [label="FIN"];
    FIN_WAIT_1 -> FIN_WAIT_2 [label="ACK"];
    CLOSE_WAIT -> LAST_ACK [label="close"];
    FIN_WAIT_2 -> TIME_WAIT [label="FIN"];
    LAST_ACK -> CLOSED [label="ACK"];
    TIME_WAIT -> CLOSED [label="timeout"];
}""",
        "category": "protocol"
    },
    {
        "name": "order_processing_fsm",
        "description": "Order processing finite state machine: new order, payment pending, processing, shipped, delivered, cancelled",
        "dot": """digraph OrderFSM {
    graph [rankdir=TB];
    node [shape=circle, style=filled];

    New [fillcolor="#C1F2C7"];
    PaymentPending [fillcolor="#FFF4C1"];
    Processing [fillcolor="#C1E4F2"];
    Shipped [fillcolor="#E4C1F2"];
    Delivered [fillcolor="#C1F2C7", shape=doublecircle];
    Cancelled [fillcolor="#FFCCCB", shape=doublecircle];

    New -> PaymentPending [label="submit"];
    PaymentPending -> Processing [label="payment received"];
    PaymentPending -> Cancelled [label="payment failed"];
    Processing -> Shipped [label="dispatched"];
    Shipped -> Delivered [label="confirmed"];
    Processing -> Cancelled [label="cancelled"];
}""",
        "category": "business_process"
    },
    {
        "name": "user_session_states",
        "description": "User session state machine: anonymous, logged in, active, idle, locked out",
        "dot": """digraph UserSession {
    graph [rankdir=LR];
    node [shape=circle];

    Anonymous -> LoggedIn [label="login"];
    LoggedIn -> Active [label="activity"];
    Active -> Idle [label="timeout"];
    Idle -> Active [label="activity"];
    Idle -> LoggedOut [label="session timeout"];
    Active -> LoggedOut [label="logout"];
    LoggedIn -> LockedOut [label="too many attempts"];
    LockedOut -> Anonymous [label="unlock"];
    LoggedOut -> Anonymous;
}""",
        "category": "authentication"
    },
    {
        "name": "document_workflow",
        "description": "Document approval workflow state machine: draft, review, approved, rejected, published",
        "dot": """digraph DocumentWorkflow {
    graph [rankdir=TB];
    node [shape=box, style="rounded,filled"];

    Draft [fillcolor="#E5F2FF"];
    Review [fillcolor="#FFF4C1"];
    Approved [fillcolor="#C1F2C7"];
    Rejected [fillcolor="#FFCCCB"];
    Published [fillcolor="#C1F2C7", shape=box];

    Draft -> Review [label="submit"];
    Review -> Approved [label="approve"];
    Review -> Rejected [label="reject"];
    Rejected -> Draft [label="revise"];
    Approved -> Published [label="publish"];
    Published -> Draft [label="new version"];
}""",
        "category": "workflow"
    },
]

output_dir = Path("/home/tim/source/activity/AnecDOT/data/raw/dot_guide_extraction")
output_dir.mkdir(parents=True, exist_ok=True)

extracted_count = 0

for example in EXAMPLES:
    try:
        print(f"Processing {example['name']}...")
        
        # Create output directory for this example
        pair_dir = output_dir / example['name']
        pair_dir.mkdir(exist_ok=True)
        
        # Save description
        (pair_dir / "description.txt").write_text(example['description'])
        
        # Save DOT
        (pair_dir / "diagram.dot").write_text(example['dot'])
        
        # Save metadata
        metadata = f"""Source: DOT Language Guide for Devs and Analysts
URL: https://www.danieleteti.it/post/dot-language-guide-for-devs-and-analysts-en/
Category: {example['category']}
Type: {example['category'].replace('_', ' ').title()}
Description: {example['description']}
"""
        (pair_dir / "metadata.txt").write_text(metadata)
        
        print(f"  ✓ Saved {example['name']} ({example['category']})")
        extracted_count += 1
        
    except Exception as e:
        print(f"  ✗ Failed to process {example['name']}: {e}")
        continue

print(f"\n{'='*70}")
print(f"Extracted {extracted_count} pairs from DOT Language Guide")
print(f"{'='*70}")
