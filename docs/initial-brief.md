# Project Graph-of-Thought: DOT as an Intermediate Reasoning Format

## 1. Executive Summary

Current Large Language Models (LLMs) often struggle with long-horizon planning and complex logical dependencies. They tend to approach coding tasks linearly (token-by-token) rather than structurally.

This project proposes introducing a formal Intermediate Representation (IR) into the LLM workflow: the DOT graph language (Graphviz). By fine-tuning an open-weights model to proficiently translate Natural Language (NL) and Code into strict DOT graphs, we aim to create a specialized "Architect Model." This model will focus solely on structural planning, dependency mapping, and state management, distinct from the actual implementation details.

The immediate goal is to build a high-quality, syntactically verified dataset and prove that a small-to-mid-sized open model (e.g., Gemma 2 9B, Llama 3 8B) can be fine-tuned to outperform larger commercial models in generating valid, logical graph structures.

## 2. Phase I: Dataset Architecture

To address the lack of public DOT training sets, we will construct a dataset using a Split-License Architecture. This separates the open-source tooling from the content, allowing for maximum legal safety regarding the Eclipse Public License (EPL) covering Graphviz documentation.

### 2.1. Repository Structure

- **Repo A (The Factory)**: Licensed MIT/Apache. Contains scrapers, parsers, prompt generators, and validation scripts. Contains no data.

- **Repo B (The Artifact)**: Licensed EPL v2.0. Contains the generated `.jsonl` training files, acknowledging them as derivative works of the Graphviz documentation and other EPL sources.

### 2.2. Data Ingestion Pipelines

We will generate `(Instruction, DOT_Output)` and `(Code, DOT_Output)` pairs from three primary streams:

#### The Documentation Stream (Foundational Syntax)

- **Source**: graphviz.org (Gallery, User Guides, Attribute references).
- **Method**: HTML scraping to extract `<description>` and `<code>` blocks.
- **Goal**: Teach the model valid syntax, attribute usage (e.g., `rankdir=LR`), and subgraph clustering.

#### The Logic Stream (Reverse Engineering)

- **Source**: Open-source repositories using FSM (Finite State Machine) libraries (e.g., `python-statemachine`, `aasm`).
- **Method**: Static analysis to extract the FSM class definition (Input) and dynamic execution to run `.to_dot()` (Output).
- **Goal**: Teach the model to abstract code logic into a visual graph.

#### The Synthetic Stream (Augmentation)

- **Source**: High-quality "seed" prompts augmented by a commercial "Teacher" LLM (Gemini/GPT-4).
- **Method**: Generate complex scenarios (e.g., "Design a microservice architecture for a bank"). The Teacher LLM generates the DOT; a generic compiler verifies it.
- **Goal**: Teach the model high-level architectural reasoning.

### 2.3. The Data Schema

The dataset will follow a strict JSONL schema to support multiple training objectives:

```json
{
  "id": "unique_id_123",
  "source": "graphviz_gallery",
  "license": "EPL-2.0",
  "task_type": "NL_TO_DOT",
  "input_text": "Create a directed graph showing a login state machine...",
  "context_snippet": null,
  "output_dot": "digraph { Start -> Login; ... }",
  "verification_status": "passed_compiler"
}
```

**Notes:**
- `task_type` can be `NL_TO_DOT` or `CODE_TO_DOT`
- `context_snippet` is optional: Code snippet or prior node output
- `verification_status` indicates compiler validation result

## 3. Phase II: Training & Validation

The objective is to validate that a locally hosted model (capable of running on consumer hardware, e.g., RTX 4090) can learn to "think" in graphs.

### 3.1. Training Setup

- **Base Models**: Gemma 2 (9B) or Llama 3 (8B).
- **Technique**: QLoRA (Quantized Low-Rank Adaptation). This allows full fine-tuning on a single 24GB VRAM GPU.
- **Objective Function**: Standard Causal Language Modeling (CLM), but heavily weighted towards the strict syntax of the DOT format.

### 3.2. Validation Protocol (The "Proof of Concept")

We will measure success by comparing the Base Model vs. the Fine-Tuned Model on a held-out test set.

#### Metric A: Syntactic Viability (Pass@1)

- **Procedure**: Generate 1,000 graphs based on unseen prompts.
- **Test**: Pipe output to `dot -Tpng > /dev/null`.
- **Success Criteria**: The Fine-Tuned model achieves >95% compilation success, whereas base models often hallucinate invalid syntax (e.g., mixing `--` and `->`).

#### Metric B: Semantic Alignment (LLM-as-a-Judge)

- **Procedure**: A stronger model (e.g., Gemini 1.5 Pro) evaluates the output.
- **Prompt**: "Does this DOT graph accurately represent the logic requested in the instruction? (Yes/No)."
- **Success Criteria**: The Fine-Tuned model shows a statistically significant improvement in logical accuracy over the Base model.

## 4. Outlook: The Application (The "Orchestrator")

**Technical Note**: This section describes the downstream application enabled by the successful completion of Phases I & II.

Once the model is proficient in generating DOT graphs, it becomes the engine for a Graph-Based Agentic Workflow.

- **The Concept**: Instead of a linear conversation, the model generates a Dependency Graph (The Plan).
- **The Execution**: A Python script (The Orchestrator) traverses this graph.
- **Context Injection**: The Orchestrator manages the "State." It treats edges as data pipelines.
  - Node A Output is captured.
  - Node B Input is constructed by injecting Node A Output into the prompt.
- **Hardware Efficiency**: This decouples the "Planner" (Local Fine-Tuned DOT Model) from the "Workers" (Specialized coding models). This allows complex, multi-step software generation to be managed entirely on local hardware with commercial-grade architectural coherence.
