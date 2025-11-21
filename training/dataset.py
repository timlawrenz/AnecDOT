"""
Dataset loader for AnecDOT training pairs.

Loads (text, DOT) pairs from multiple sources:
- data/training/statemachine_cat/pairs.json
- data/*.jsonl streams (synthetic, logic, documentation, attribute-docs)
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datasets import Dataset
import random


class AnecDOTDataset:
    """Loads and preprocesses AnecDOT training pairs."""
    
    def __init__(self, data_dir: str = "data", seed: int = 42):
        self.data_dir = Path(data_dir)
        self.seed = seed
        random.seed(seed)
        
    def load_pairs_json(self) -> List[Dict]:
        """Load pairs from statemachine_cat pairs.json."""
        pairs_file = self.data_dir / "training/statemachine_cat/pairs.json"
        if not pairs_file.exists():
            return []
        
        with open(pairs_file) as f:
            data = json.load(f)
            
        pairs = []
        for item in data:
            # statemachine_cat uses 'code' and 'dot' field names
            if "code" in item and "dot" in item:
                pairs.append({
                    "input_text": item["code"],
                    "output_dot": item["dot"],
                    "source": "statemachine_cat"
                })
        
        return pairs
    
    def load_jsonl_streams(self) -> List[Dict]:
        """Load pairs from JSONL stream files."""
        stream_files = [
            "synthetic-stream.jsonl",
            "logic-stream.jsonl",
            "documentation-stream.jsonl",
            "attribute-docs-stream.jsonl",
            "error-correction-stream.jsonl"
        ]
        
        pairs = []
        for stream_file in stream_files:
            stream_path = self.data_dir / stream_file
            if not stream_path.exists():
                continue
                
            with open(stream_path) as f:
                for line in f:
                    try:
                        item = json.loads(line)
                        if "input_text" in item and "output_dot" in item:
                            pairs.append({
                                "input_text": item["input_text"],
                                "output_dot": item["output_dot"],
                                "source": item.get("source", stream_file)
                            })
                    except json.JSONDecodeError:
                        continue
        
        return pairs
    
    def load_all(self) -> List[Dict]:
        """Load all training pairs from all sources."""
        pairs = []
        pairs.extend(self.load_pairs_json())
        pairs.extend(self.load_jsonl_streams())
        
        # Shuffle to mix sources
        random.shuffle(pairs)
        
        return pairs
    
    def format_instruction(self, pair: Dict, tokenizer=None) -> str:
        """Format pair as instruction-tuning prompt.
        
        If tokenizer provided, uses its chat template.
        Otherwise uses Gemma-2B-IT format as default.
        """
        if tokenizer and hasattr(tokenizer, 'apply_chat_template'):
            # Use model's native chat template
            messages = [
                {"role": "user", "content": pair["input_text"]}
            ]
            # Format without assistant response (we'll add that)
            prompt = tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            # Add the assistant's response
            formatted = prompt + pair["output_dot"]
        else:
            # Gemma-2B-IT format (fallback)
            formatted = (
                f"<bos><start_of_turn>user\n"
                f"{pair['input_text']}<end_of_turn>\n"
                f"<start_of_turn>model\n"
                f"{pair['output_dot']}"
            )
        
        return formatted
    
    def create_dataset(self, train_val_split: float = 0.9, tokenizer=None) -> Dict[str, Dataset]:
        """Create train/validation HuggingFace datasets.
        
        Args:
            train_val_split: Fraction of data for training
            tokenizer: Optional tokenizer for chat template formatting
        """
        all_pairs = self.load_all()
        
        if not all_pairs:
            raise ValueError("No training pairs found in data directory")
        
        # Filter out any pairs with None values
        valid_pairs = [p for p in all_pairs if p.get("input_text") and p.get("output_dot")]
        
        if not valid_pairs:
            raise ValueError("No valid pairs found (all have None values)")
        
        # Format as instructions
        formatted = [
            {
                "text": self.format_instruction(pair, tokenizer),
                "input_text": pair["input_text"],
                "output_dot": pair["output_dot"],
                "source": pair["source"]
            }
            for pair in valid_pairs
        ]
        
        # Split into train/val
        split_idx = int(len(formatted) * train_val_split)
        train_data = formatted[:split_idx]
        val_data = formatted[split_idx:]
        
        # Create HuggingFace datasets
        train_dataset = Dataset.from_list(train_data)
        val_dataset = Dataset.from_list(val_data)
        
        print(f"Loaded {len(train_data)} training examples, {len(val_data)} validation examples")
        print(f"Sources: {set(pair['source'] for pair in valid_pairs)}")
        
        return {
            "train": train_dataset,
            "validation": val_dataset
        }
    
    def get_statistics(self) -> Dict:
        """Get dataset statistics."""
        pairs = self.load_all()
        
        if not pairs:
            return {"error": "No pairs found"}
        
        # Filter out any pairs with None values
        valid_pairs = [p for p in pairs if p.get("input_text") and p.get("output_dot")]
        
        if not valid_pairs:
            return {"error": "No valid pairs found (all have None values)"}
        
        input_lengths = [len(p["input_text"]) for p in valid_pairs]
        output_lengths = [len(p["output_dot"]) for p in valid_pairs]
        sources = {}
        
        for pair in valid_pairs:
            source = pair["source"]
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_pairs": len(valid_pairs),
            "avg_input_length": sum(input_lengths) / len(input_lengths),
            "avg_output_length": sum(output_lengths) / len(output_lengths),
            "sources": sources
        }


if __name__ == "__main__":
    # Test dataset loading
    dataset = AnecDOTDataset()
    stats = dataset.get_statistics()
    
    print("Dataset Statistics:")
    print(f"  Total pairs: {stats['total_pairs']}")
    print(f"  Avg input length: {stats['avg_input_length']:.0f} chars")
    print(f"  Avg output length: {stats['avg_output_length']:.0f} chars")
    print(f"  Sources: {stats['sources']}")
    
    print("\nCreating train/val split...")
    datasets = dataset.create_dataset()
    print(f"  Train: {len(datasets['train'])} examples")
    print(f"  Validation: {len(datasets['validation'])} examples")
