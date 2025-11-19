"""
Simple prompt template for DOT generation.

Based on analysis of existing 58 examples:
- Focus on 2-10 node graphs
- Simple state machines
- Directed graphs only
- Basic styling patterns we've seen work
"""

FEW_SHOT_EXAMPLE = """
Example 1 - Traffic Light State Machine:

Input: "A traffic light machine that cycles through green, yellow, and red states."

Output DOT:
```dot
digraph TrafficLight {
    rankdir=LR;
    
    green [label="Green", shape=rectangle, style="rounded,filled", fillcolor=lightgreen];
    yellow [label="Yellow", shape=rectangle, style="rounded,filled", fillcolor=yellow];
    red [label="Red", shape=rectangle, style="rounded,filled", fillcolor=lightcoral];
    
    green -> yellow [label="timer"];
    yellow -> red [label="timer"];
    red -> green [label="timer"];
}
```
"""

SYSTEM_PROMPT = """You are a DOT graph generator. Given a description of a state machine or workflow, generate a valid Graphviz DOT file.

RULES:
1. Use 'digraph' for directed graphs
2. Keep it simple: 2-10 nodes maximum
3. Use clear, descriptive node labels
4. Add basic styling (shapes, colors) where appropriate
5. Label all edges with transition names
6. Output ONLY the DOT code, no explanations
7. Ensure the DOT is valid and will compile

STYLE PATTERNS TO USE:
- Node shapes: rectangle, ellipse, circle
- Node styles: "rounded,filled", "filled"
- Colors: lightblue, lightgreen, yellow, lightcoral, white
- Graph attributes: rankdir=LR (left to right layout)

DO NOT USE:
- Subgraphs or clusters (too complex)
- More than 10 nodes (too large)
- Undirected graphs
- Advanced DOT features

{few_shot_examples}

Now generate a DOT graph for this description:
{prompt}

Output only the DOT code:"""


def get_prompt(description: str) -> str:
    """Generate the full prompt for DOT generation.
    
    Args:
        description: Natural language description of the graph to generate
        
    Returns:
        Complete prompt with system instructions and few-shot examples
    """
    return SYSTEM_PROMPT.format(
        few_shot_examples=FEW_SHOT_EXAMPLE,
        prompt=description
    )


# Simple domain-specific prompts based on our existing examples
SIMPLE_PROMPTS = [
    # Similar to traffic light (we have this pattern)
    "A door controller with states: closed, opening, open, closing. Include transitions for 'open_button', 'opened', 'close_button', and 'closed'.",
    
    "A light switch with two states: on and off. Include a 'toggle' transition between them.",
    
    "A player character state machine with states: idle, walking, running, jumping. Add appropriate transitions.",
    
    "An order status workflow with states: pending, processing, shipped, delivered. Include state transitions.",
    
    "A login authentication flow with states: logged_out, logging_in, logged_in, session_expired.",
    
    "A coffee machine with states: idle, brewing, ready, cleaning. Add transitions for making coffee.",
    
    "A phone call state machine: idle, ringing, active, on_hold, ended.",
    
    "An elevator controller with states: idle, moving_up, moving_down, doors_open, emergency_stop.",
    
    "A TCP connection state machine: closed, listen, syn_sent, established, close_wait.",
    
    "A vending machine with states: idle, item_selected, payment_pending, dispensing, change_returned.",
]


def get_test_prompts(count: int = 10) -> list[str]:
    """Get a set of test prompts for validation.
    
    Args:
        count: Number of prompts to return (max 10 for now)
        
    Returns:
        List of natural language prompts
    """
    return SIMPLE_PROMPTS[:min(count, len(SIMPLE_PROMPTS))]
