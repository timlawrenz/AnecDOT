"""
Sandboxed execution environment for extracting DOT from FSM instances.

Uses subprocess isolation with timeout and resource limits to safely
execute FSM library code and capture DOT output.
"""

import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DotExtractionResult:
    """Result of DOT extraction from FSM code.
    
    Attributes:
        success: True if DOT was successfully extracted
        dot_output: DOT string (if successful)
        error_message: Error description (if failed)
        execution_time: Time taken in seconds
    """
    success: bool
    dot_output: Optional[str] = None
    error_message: Optional[str] = None
    execution_time: float = 0.0


class FSMSandbox:
    """Isolated execution environment for FSM DOT extraction."""
    
    def __init__(self, timeout: int = 30):
        """Initialize sandbox.
        
        Args:
            timeout: Maximum execution time in seconds
        """
        self.timeout = timeout
    
    def extract_dot_from_statemachine(self, source_code: str) -> DotExtractionResult:
        """Extract DOT from python-statemachine code.
        
        Args:
            source_code: Python code defining a StateMachine
            
        Returns:
            DotExtractionResult with DOT output or error
        """
        wrapper_code = textwrap.dedent(f'''
import sys
try:
    # Original code
{textwrap.indent(source_code, "    ")}
    
    # Try to instantiate and extract DOT
    import inspect
    from statemachine import StateMachine
    
    # Find StateMachine subclasses
    local_vars = dict(locals())
    for name, obj in local_vars.items():
        if inspect.isclass(obj) and issubclass(obj, StateMachine) and obj is not StateMachine:
            try:
                instance = obj()
                graph = instance._graph()
                dot_output = graph.to_string()
                print("__DOT_START__")
                print(dot_output)
                print("__DOT_END__")
                sys.exit(0)
            except Exception as e:
                print(f"__ERROR__Failed to extract DOT: {{e}}", file=sys.stderr)
                sys.exit(1)
    
    print("__ERROR__No StateMachine subclass found", file=sys.stderr)
    sys.exit(1)
    
except Exception as e:
    import traceback
    print(f"__ERROR__Execution failed: {{e}}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
        ''')
        
        return self._execute_code(wrapper_code)
    
    def extract_dot_from_transitions(self, source_code: str) -> DotExtractionResult:
        """Extract DOT from transitions GraphMachine code.
        
        Args:
            source_code: Python code using GraphMachine
            
        Returns:
            DotExtractionResult with DOT output or error
        """
        wrapper_code = textwrap.dedent(f'''
import sys
try:
    # Original code
{textwrap.indent(source_code, "    ")}
    
    # Try to find GraphMachine instances
    from transitions.extensions import GraphMachine
    
    # Look for machine variable
    local_vars = dict(locals())
    for name, obj in local_vars.items():
        if isinstance(obj, GraphMachine):
            try:
                graph = obj.get_graph()
                dot_output = graph.source
                print("__DOT_START__")
                print(dot_output)
                print("__DOT_END__")
                sys.exit(0)
            except Exception as e:
                import traceback
                print(f"__ERROR__Failed to extract DOT: {{e}}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                sys.exit(1)
    
    print("__ERROR__No GraphMachine instance found", file=sys.stderr)
    sys.exit(1)
    
except Exception as e:
    import traceback
    print(f"__ERROR__Execution failed: {{e}}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
        ''')
        
        return self._execute_code(wrapper_code)
    
    def _execute_code(self, code: str) -> DotExtractionResult:
        """Execute Python code in isolated subprocess.
        
        Args:
            code: Python code to execute
            
        Returns:
            DotExtractionResult with output or error
        """
        import time
        
        start_time = time.time()
        
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # Write code to temporary file
                code_file = Path(tmpdir) / "extract.py"
                code_file.write_text(code)
                
                # Execute in subprocess with timeout
                result = subprocess.run(
                    [sys.executable, str(code_file)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=tmpdir,
                    env={
                        'PYTHONPATH': str(Path.cwd()),
                        'PATH': sys.path[0]
                    }
                )
                
                execution_time = time.time() - start_time
                
                # Parse output
                if "__DOT_START__" in result.stdout:
                    lines = result.stdout.splitlines()
                    start_idx = None
                    end_idx = None
                    
                    for i, line in enumerate(lines):
                        if line == "__DOT_START__":
                            start_idx = i + 1
                        elif line == "__DOT_END__":
                            end_idx = i
                            break
                    
                    if start_idx is not None and end_idx is not None:
                        dot_output = '\n'.join(lines[start_idx:end_idx])
                        return DotExtractionResult(
                            success=True,
                            dot_output=dot_output,
                            execution_time=execution_time
                        )
                
                # Extract error message
                error_msg = "Unknown error"
                if "__ERROR__" in result.stderr:
                    for line in result.stderr.splitlines():
                        if "__ERROR__" in line:
                            error_msg = line.replace("__ERROR__", "").strip()
                            break
                elif result.stderr:
                    error_msg = result.stderr[:200]
                
                return DotExtractionResult(
                    success=False,
                    error_message=error_msg,
                    execution_time=execution_time
                )
                
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return DotExtractionResult(
                success=False,
                error_message=f"Execution timeout ({self.timeout}s)",
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return DotExtractionResult(
                success=False,
                error_message=f"Sandbox error: {e}",
                execution_time=execution_time
            )
