"""
Improved prompt templates for Phase II.2.6 training.

Based on showcase analysis revealing issues:
1. Excessive styling/formatting hallucination
2. Missing states from prompt
3. Invalid DOT syntax (fill=, shape on edges)
4. Hallucinated labels, timing, colors

New approach:
- Clearer constraints
- "Unless specified" flexibility
- Example-driven
- Minimal output focus
"""

# Base instruction that precedes all prompts
BASE_INSTRUCTION = """Generate valid Graphviz DOT code for the described state machine.

Requirements:
- Output ONLY the DOT code, no explanations or comments
- Use simple node and edge declarations
- Do not add labels, colors, or styling unless specified
- Ensure all mentioned states and transitions are included
- Use standard DOT syntax only

Example format:
digraph name {
  StateA -> StateB;
  StateB -> StateC;
}

Task: """


# Alternative minimal instruction
MINIMAL_INSTRUCTION = """Create a DOT digraph with the specified states and transitions. Use simple syntax without extra formatting unless requested.

Example:
digraph { A -> B; B -> C; }

Task: """


# For code-to-DOT tasks
CODE_TO_DOT_INSTRUCTION = """Generate a DOT state diagram representing the state machine in this code.

Requirements:
- Extract states and transitions only
- Use simple DOT syntax
- No styling unless the code specifies it

Code:
"""


# For natural language to DOT
NL_TO_DOT_INSTRUCTION = """Generate a DOT digraph for the following state machine description. Use minimal syntax.

Description: """


def format_prompt(user_request: str, task_type: str = "nl_to_dot") -> str:
    """
    Format a user request with appropriate instruction prefix.
    
    Args:
        user_request: The actual state machine description or code
        task_type: Type of task - "nl_to_dot", "code_to_dot", or "error_correction"
    
    Returns:
        Formatted prompt ready for training
    """
    
    if task_type == "code_to_dot":
        return CODE_TO_DOT_INSTRUCTION + user_request
    elif task_type == "error_correction":
        # Error correction uses different format
        return f"Fix the syntax errors in this DOT code:\n\n{user_request}"
    else:  # nl_to_dot (default)
        return BASE_INSTRUCTION + user_request


# Test examples
if __name__ == "__main__":
    # Test NL to DOT
    nl_example = "Create a traffic light with Green, Yellow, Red states cycling in order."
    print("NL TO DOT:")
    print(format_prompt(nl_example))
    print("\n" + "="*70 + "\n")
    
    # Test CODE to DOT
    code_example = """
class TrafficLight:
    def __init__(self):
        self.state = "Green"
    
    def change(self):
        if self.state == "Green":
            self.state = "Yellow"
        elif self.state == "Yellow":
            self.state = "Red"
        else:
            self.state = "Green"
"""
    print("CODE TO DOT:")
    print(format_prompt(code_example, "code_to_dot"))
    print("\n" + "="*70 + "\n")
    
    # Test ERROR CORRECTION
    error_example = """digraph traffic {
  Green -> Yellow
  Yellow -> Red;
  Red -> Green
}"""
    print("ERROR CORRECTION:")
    print(format_prompt(error_example, "error_correction"))
