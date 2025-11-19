"""
Synthetic DOT generator - Command-line interface.

Minimal implementation for Phase I.3 validation.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from .generator import create_generator, GenerationResult
from .templates import get_prompt, get_test_prompts
from .validator import validate_dot_syntax, create_training_pair, write_jsonl, calculate_cost


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic DOT training pairs using teacher LLMs"
    )
    
    parser.add_argument(
        "--provider",
        choices=["gemini-flash", "gemini-pro", "gemini-3", "ollama-gemma", "ollama-deepseek"],
        default="ollama-gemma",
        help="LLM provider to use (default: ollama-gemma for free local generation)"
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of examples to generate (default: 10)"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/synthetic-stream.jsonl"),
        help="Output JSONL file (default: data/synthetic-stream.jsonl)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without calling LLM"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    args = parser.parse_args()
    
    # Get prompts
    prompts = get_test_prompts(args.count)
    
    if args.dry_run:
        print(f"Would generate {len(prompts)} examples using {args.provider}")
        print(f"\nSample prompts:")
        for i, prompt in enumerate(prompts[:3], 1):
            print(f"  {i}. {prompt[:80]}...")
        print(f"\nOutput would be written to: {args.output}")
        return 0
    
    # Create generator
    print(f"Initializing {args.provider}...")
    try:
        generator = create_generator(args.provider)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    # Generate
    print(f"Generating {len(prompts)} examples...")
    print(f"Provider: {args.provider}")
    print(f"Output: {args.output}")
    print()
    
    results = []
    successful = 0
    failed = 0
    total_cost = 0.0
    
    for i, description in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] {description[:60]}...")
        
        # Build full prompt
        full_prompt = get_prompt(description)
        
        # Generate
        result = generator.generate(full_prompt)
        
        if not result.success:
            print(f"  ❌ Generation failed: {result.error}")
            failed += 1
            continue
        
        # Validate
        is_valid, error = validate_dot_syntax(result.dot_output)
        
        if is_valid:
            print(f"  ✓ Generated and validated")
            successful += 1
            
            # Create training pair
            pair = create_training_pair(
                prompt=description,
                dot_output=result.dot_output,
                provider=result.provider,
                model=result.model,
                validation_passed=True
            )
            results.append(pair)
            
            if args.verbose:
                print(f"    Nodes: {result.dot_output.count('[')}")
                print(f"    Edges: {result.dot_output.count('->')}")
            
        else:
            print(f"  ❌ Validation failed: {error[:60]}...")
            failed += 1
            
            if args.verbose:
                print(f"    Generated DOT:")
                print("    " + "\n    ".join(result.dot_output.split('\n')[:5]))
        
        # Track cost
        if result.tokens_used:
            cost = calculate_cost(result.tokens_used, result.provider, result.model)
            total_cost += cost
            
            if args.verbose and cost > 0:
                print(f"    Cost: ${cost:.6f}")
        
        print()
    
    # Write results
    if results:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        write_jsonl(results, args.output, append=False)
    
    # Summary
    print("="*70)
    print("GENERATION SUMMARY")
    print("="*70)
    print(f"Total prompts:  {len(prompts)}")
    print(f"Successful:     {successful} ({100*successful/len(prompts):.1f}%)")
    print(f"Failed:         {failed}")
    print(f"Total cost:     ${total_cost:.6f}")
    if total_cost > 0:
        print(f"Cost per pair:  ${total_cost/successful:.6f}")
    print(f"\nOutput written to: {args.output}")
    print("="*70)
    
    # Validation check
    if successful < len(prompts) * 0.5:
        print("\n⚠️  WARNING: Less than 50% success rate!")
        print("   Consider trying a different provider or refining prompts.")
        return 1
    
    if successful >= len(prompts) * 0.8:
        print("\n✅ Great success rate! Synthetic generation is working well.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
