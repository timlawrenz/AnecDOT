"""
Improved prompt engineering for DOT graph generation.

Based on Phase II.2 failure analysis, provides better prompts to reduce:
- Quote/escape errors
- Wrong edge operators  
- Incomplete output
"""

# Base prompt with explicit constraints
IMPROVED_SYSTEM_PROMPT = """You are a Graphviz DOT code generator. Generate ONLY valid DOT code.

CRITICAL RULES:
1. Use double quotes (") for all names and labels, NEVER backticks (`)
2. In digraph, use -> for edges (NOT --)
3. Complete the graph with closing brace }
4. Keep it simple - avoid complex HTML labels unless necessary
5. Output ONLY the DOT code, no explanations

Example format:
digraph "MyGraph" {
  rankdir=LR;
  A [label="State A"];
  B [label="State B"];
  A -> B [label="transition"];
}

Now generate valid DOT code for:"""


# Simpler prompt without HTML labels
SIMPLE_PROMPT = """Generate a valid Graphviz DOT graph using this format:

digraph "GraphName" {
  node [shape=rectangle style="rounded,filled" fillcolor=lightblue];
  
  A [label="Label A"];
  B [label="Label B"];
  
  A -> B [label="edge label"];
}

Requirements:
- Use double quotes for names/labels
- Use -> for directed edges
- Include closing brace }
- Keep labels simple (no HTML)

Task:"""


# Constrained prompt for FSMs
FSM_PROMPT = """Generate a Graphviz DOT state machine diagram.

Format requirements:
- Start with: digraph "StateMachineName" {
- Nodes: StateName [label="Display Name"];
- Edges: Source -> Target [label="transition"];
- End with: }

Use simple text labels only (no HTML/tables).

State machine to generate:"""


def get_improved_prompt(description: str, prompt_type: str = "improved") -> str:
    """Get improved prompt for DOT generation.
    
    Args:
        description: Natural language description of graph to generate
        prompt_type: Type of prompt ("improved", "simple", "fsm")
        
    Returns:
        Full prompt with constraints
    """
    prompts = {
        "improved": IMPROVED_SYSTEM_PROMPT,
        "simple": SIMPLE_PROMPT,
        "fsm": FSM_PROMPT
    }
    
    base_prompt = prompts.get(prompt_type, IMPROVED_SYSTEM_PROMPT)
    return f"{base_prompt}\n\n{description}"


# Few-shot examples to reduce errors
FEW_SHOT_EXAMPLES = """
GOOD EXAMPLE 1:
Task: Traffic light state machine
Output:
digraph "TrafficLight" {
  rankdir=LR;
  Green [label="Green Light"];
  Yellow [label="Yellow Light"];
  Red [label="Red Light"];
  Green -> Yellow [label="timer"];
  Yellow -> Red [label="timer"];
  Red -> Green [label="timer"];
}

GOOD EXAMPLE 2:
Task: Login flow
Output:
digraph "Login" {
  LoggedOut [label="Logged Out"];
  LoggingIn [label="Logging In"];
  LoggedIn [label="Logged In"];
  LoggedOut -> LoggingIn [label="submit credentials"];
  LoggingIn -> LoggedIn [label="success"];
  LoggingIn -> LoggedOut [label="failure"];
}

BAD EXAMPLE (DO NOT DO):
digraph `MyGraph` {  // WRONG: use "MyGraph" not `MyGraph`
  a -- b;  // WRONG: use -> not -- in digraph
  c [label="test\l"];  // WRONG: avoid \l escape
// WRONG: missing closing }

Now generate:"""


def get_few_shot_prompt(description: str) -> str:
    """Get prompt with few-shot examples.
    
    Args:
        description: Natural language description
        
    Returns:
        Prompt with examples showing correct/incorrect patterns
    """
    return f"{FEW_SHOT_EXAMPLES}\n\n{description}"


# Prompt specifically to avoid common errors
ERROR_AWARE_PROMPT = """Generate valid Graphviz DOT code.

AVOID THESE COMMON MISTAKES:
❌ Using backticks: digraph `name` 
✅ Use quotes: digraph "name"

❌ Wrong edge operator in digraph: a -- b
✅ Use directed arrow: a -> b

❌ Incomplete graph (missing })
✅ Always close with }

❌ Complex HTML labels (often break)
✅ Use simple text labels

Generate DOT for:"""


def compare_prompts():
    """Compare different prompt approaches."""
    
    test_description = "A simple FSM with states A, B, C. A->B on 'start', B->C on 'finish'."
    
    print("PROMPT COMPARISON")
    print("=" * 70)
    
    prompts = {
        "Improved": get_improved_prompt(test_description),
        "Simple": get_improved_prompt(test_description, "simple"),
        "FSM-specific": get_improved_prompt(test_description, "fsm"),
        "Few-shot": get_few_shot_prompt(test_description),
    }
    
    for name, prompt in prompts.items():
        print(f"\n{name} Prompt:")
        print("-" * 70)
        print(prompt[:300] + "..." if len(prompt) > 300 else prompt)
    
    print("\n" + "=" * 70)
    print("Recommendation: Test 'Few-shot' and 'Error-aware' in evaluation")


if __name__ == "__main__":
    compare_prompts()
