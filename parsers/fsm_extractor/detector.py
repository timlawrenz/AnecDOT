"""
Static analysis for detecting FSM library usage patterns.

Analyzes Python source code to identify state machine definitions from:
- python-statemachine: StateMachine subclasses
- transitions: Machine and GraphMachine instantiations
"""

import ast
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path


@dataclass
class FSMMatch:
    """Represents a detected FSM pattern in source code.
    
    Attributes:
        library: FSM library name ("python-statemachine" or "transitions")
        class_name: Name of the state machine class (if class-based)
        start_line: Starting line number in source file
        end_line: Ending line number in source file
        source_code: Extracted source code for the FSM definition
        has_graph_support: True if library supports graph export
    """
    library: str
    class_name: Optional[str]
    start_line: int
    end_line: int
    source_code: str
    has_graph_support: bool


class FSMDetector(ast.NodeVisitor):
    """AST visitor for detecting FSM library usage patterns."""
    
    def __init__(self, source_code: str):
        """Initialize detector with source code.
        
        Args:
            source_code: Python source code to analyze
        """
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.matches: List[FSMMatch] = []
        
        # Track imports
        self.has_statemachine_import = False
        self.has_transitions_import = False
        self.has_graphmachine_import = False
        
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Track imports of FSM libraries."""
        if node.module == 'statemachine':
            self.has_statemachine_import = True
        elif node.module == 'transitions':
            self.has_transitions_import = True
            # Check if GraphMachine is imported
            for alias in node.names:
                if alias.name == 'Machine':
                    self.has_transitions_import = True
        elif node.module == 'transitions.extensions':
            for alias in node.names:
                if alias.name == 'GraphMachine':
                    self.has_graphmachine_import = True
        
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Detect StateMachine subclasses."""
        if self.has_statemachine_import:
            # Check if class inherits from StateMachine
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == 'StateMachine':
                    source_code = self._extract_node_source(node)
                    self.matches.append(FSMMatch(
                        library="python-statemachine",
                        class_name=node.name,
                        start_line=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        source_code=source_code,
                        has_graph_support=True
                    ))
                    break
        
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call) -> None:
        """Detect Machine/GraphMachine instantiations."""
        if isinstance(node.func, ast.Name):
            # Check for Machine() or GraphMachine() calls
            if node.func.id == 'Machine' and self.has_transitions_import:
                # Base Machine - no graph support
                source_code = self._extract_call_with_context(node)
                self.matches.append(FSMMatch(
                    library="transitions",
                    class_name=None,
                    start_line=node.lineno,
                    end_line=node.end_lineno or node.lineno,
                    source_code=source_code,
                    has_graph_support=False
                ))
            elif node.func.id == 'GraphMachine' and self.has_graphmachine_import:
                # GraphMachine - has graph support
                source_code = self._extract_call_with_context(node)
                self.matches.append(FSMMatch(
                    library="transitions",
                    class_name=None,
                    start_line=node.lineno,
                    end_line=node.end_lineno or node.lineno,
                    source_code=source_code,
                    has_graph_support=True
                ))
        
        self.generic_visit(node)
    
    def _extract_call_with_context(self, node: ast.Call) -> str:
        """Extract a function call with surrounding context for transitions.
        
        For transitions, we need more context (variable definitions, etc.)
        """
        # Get surrounding lines (up to 20 lines before the call)
        start_line = max(0, node.lineno - 21)
        end_line = node.end_lineno or node.lineno
        
        # Find actual start (first non-comment, non-empty line before call)
        actual_start = start_line
        for i in range(node.lineno - 2, start_line - 1, -1):
            if i < 0 or i >= len(self.source_lines):
                break
            line = self.source_lines[i].strip()
            if line and not line.startswith('#'):
                actual_start = i
            else:
                break
        
        # Extract lines
        context_lines = self.source_lines[actual_start:end_line]
        
        # Add imports
        import_lines = []
        for line in self.source_lines[:actual_start]:
            stripped = line.strip()
            if (stripped.startswith('from transitions') or
                stripped.startswith('import transitions')):
                import_lines.append(line)
        
        if import_lines:
            result = '\n'.join(import_lines) + '\n\n' + '\n'.join(context_lines)
        else:
            result = '\n'.join(context_lines)
        
        return result
    
    def _extract_node_source(self, node: ast.AST) -> str:
        """Extract source code for an AST node with necessary imports."""
        start_line = node.lineno - 1  # 0-indexed
        end_line = (node.end_lineno or node.lineno)
        
        # Get lines for this node
        node_lines = self.source_lines[start_line:end_line]
        
        # Also extract relevant imports (statemachine or transitions)
        import_lines = []
        for i, line in enumerate(self.source_lines[:start_line]):
            stripped = line.strip()
            if (stripped.startswith('from statemachine import') or
                stripped.startswith('from transitions') or  
                stripped.startswith('import statemachine') or
                stripped.startswith('import transitions')):
                import_lines.append(line)
        
        # Combine imports + node code
        if import_lines:
            result = '\n'.join(import_lines) + '\n\n' + '\n'.join(node_lines)
        else:
            result = '\n'.join(node_lines)
        
        return result


def detect_fsm_patterns(file_path: Path) -> List[FSMMatch]:
    """Detect FSM library usage in a Python file.
    
    Args:
        file_path: Path to Python source file
        
    Returns:
        List of FSMMatch objects for detected patterns
        
    Raises:
        SyntaxError: If file contains invalid Python syntax
    """
    try:
        source_code = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # Skip binary files
        return []
    
    try:
        tree = ast.parse(source_code, filename=str(file_path))
    except SyntaxError:
        # Skip files with syntax errors
        return []
    
    detector = FSMDetector(source_code)
    detector.visit(tree)
    
    return detector.matches


def has_fsm_imports(file_path: Path) -> bool:
    """Quick check if file imports FSM libraries (without full AST analysis).
    
    Args:
        file_path: Path to Python source file
        
    Returns:
        True if file contains FSM library imports
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        return (
            'from statemachine import' in content or
            'from transitions import' in content or
            'from transitions.extensions import GraphMachine' in content
        )
    except (UnicodeDecodeError, OSError):
        return False
