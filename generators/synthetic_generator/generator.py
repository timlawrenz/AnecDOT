"""
Core DOT generation logic with multiple LLM providers.

Minimal implementation for Phase I.3 validation.
"""

import os
import re
import json
import hashlib
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GenerationResult:
    """Result of a single DOT generation attempt."""
    prompt: str
    dot_output: str
    success: bool
    error: Optional[str] = None
    provider: str = ""
    model: str = ""
    tokens_used: Optional[Dict[str, int]] = None


class BaseGenerator:
    """Base class for LLM generators."""
    
    def __init__(self, model: str):
        self.model = model
        
    def generate(self, prompt: str) -> GenerationResult:
        """Generate DOT from a prompt.
        
        Args:
            prompt: Complete prompt including system instructions
            
        Returns:
            GenerationResult with DOT output or error
        """
        raise NotImplementedError


class GeminiGenerator(BaseGenerator):
    """Generator using Google Gemini API."""
    
    def __init__(self, model: str = "gemini-2.5-flash"):
        super().__init__(model)
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
    
    def generate(self, prompt: str) -> GenerationResult:
        """Generate using Gemini API."""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            
            response = model.generate_content(prompt)
            
            # Extract DOT code from response
            dot_output = self._extract_dot(response.text)
            
            if not dot_output:
                return GenerationResult(
                    prompt=prompt,
                    dot_output="",
                    success=False,
                    error="No DOT code found in response",
                    provider="gemini",
                    model=self.model
                )
            
            return GenerationResult(
                prompt=prompt,
                dot_output=dot_output,
                success=True,
                provider="gemini",
                model=self.model,
                tokens_used={
                    "input": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "output": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0
                }
            )
            
        except Exception as e:
            return GenerationResult(
                prompt=prompt,
                dot_output="",
                success=False,
                error=str(e),
                provider="gemini",
                model=self.model
            )
    
    def _extract_dot(self, text: str) -> str:
        """Extract DOT code from model response.
        
        Handles various markdown formats:
        - ```dot ... ```
        - ```graphviz ... ```
        - ``` ... ```
        - Plain text with digraph/graph
        """
        # Try code blocks first
        patterns = [
            r'```(?:dot|graphviz)?\s*(digraph[^`]+)```',
            r'```\s*(digraph[^`]+)```',
            r'(digraph\s+\w+\s*\{[^}]+\})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # If no match, check if the whole response looks like DOT
        if text.strip().startswith('digraph'):
            return text.strip()
        
        return ""


class OllamaGenerator(BaseGenerator):
    """Generator using local Ollama models."""
    
    def __init__(self, model: str = "gemma3:27b"):
        super().__init__(model)
        self._check_ollama_available()
    
    def _check_ollama_available(self):
        """Check if Ollama is running."""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code != 200:
                raise ValueError("Ollama is not running. Start it with: ollama serve")
        except requests.exceptions.RequestException:
            raise ValueError("Cannot connect to Ollama. Is it running? (ollama serve)")
    
    def generate(self, prompt: str) -> GenerationResult:
        """Generate using Ollama API."""
        try:
            import requests
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code != 200:
                return GenerationResult(
                    prompt=prompt,
                    dot_output="",
                    success=False,
                    error=f"Ollama API error: {response.status_code}",
                    provider="ollama",
                    model=self.model
                )
            
            result = response.json()
            text = result.get("response", "")
            
            # Extract DOT code
            dot_output = self._extract_dot(text)
            
            if not dot_output:
                return GenerationResult(
                    prompt=prompt,
                    dot_output="",
                    success=False,
                    error="No DOT code found in response",
                    provider="ollama",
                    model=self.model
                )
            
            return GenerationResult(
                prompt=prompt,
                dot_output=dot_output,
                success=True,
                provider="ollama",
                model=self.model
            )
            
        except Exception as e:
            return GenerationResult(
                prompt=prompt,
                dot_output="",
                success=False,
                error=str(e),
                provider="ollama",
                model=self.model
            )
    
    def _extract_dot(self, text: str) -> str:
        """Extract DOT code (same logic as Gemini)."""
        patterns = [
            r'```(?:dot|graphviz)?\s*(digraph[^`]+)```',
            r'```\s*(digraph[^`]+)```',
            r'(digraph\s+\w+\s*\{[^}]+\})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        if text.strip().startswith('digraph'):
            return text.strip()
        
        return ""


def create_generator(provider: str = "gemini-flash") -> BaseGenerator:
    """Factory function to create the appropriate generator.
    
    Args:
        provider: One of 'gemini-flash', 'gemini-pro', 'gemini-3', 
                  'ollama-gemma', 'ollama-deepseek'
    
    Returns:
        Configured generator instance
    
    Raises:
        ValueError: If provider is unknown or not configured
    """
    if provider == "gemini-flash":
        return GeminiGenerator("gemini-2.5-flash")
    elif provider == "gemini-pro":
        return GeminiGenerator("gemini-2.5-pro")
    elif provider == "gemini-3":
        return GeminiGenerator("gemini-3-pro-preview")
    elif provider == "ollama-gemma":
        return OllamaGenerator("gemma3:27b")
    elif provider == "ollama-deepseek":
        return OllamaGenerator("deepseek-r1:32b")
    else:
        raise ValueError(
            f"Unknown provider: {provider}. "
            f"Choose from: gemini-flash, gemini-pro, gemini-3, ollama-gemma, ollama-deepseek"
        )
