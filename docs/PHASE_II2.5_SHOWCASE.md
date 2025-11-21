# Phase II.2.5 Visual Results Showcase

**Date:** 2025-11-21  
**Model:** google/gemma-2b-it  
**Training:** Phase II.2.5 (450 pairs with error correction)  

---

## Summary

- **Test prompts:** 8
- **Base model success:** 6/8 (75.0%)
- **Fine-tuned success:** 7/8 (87.5%)
- **Improvement:** +1 examples

---

## Test 1: Simple FSM

### Prompt

> Generate valid Graphviz DOT code for the described state machine.

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

Task: Create a state machine for a traffic light with three states: Green, Yellow, and Red. Green transitions to Yellow, Yellow to Red, and Red back to Green.

### Base Model Output

❌ **Failed to generate valid DOT**

<details>
<summary>Raw output (click to expand)</summary>

```
```dot
digraph traffic_light {
  StateA --> StateYellow;
  StateYellow --> StateRed;
  StateRed --> StateA;
}
```
```

</details>

### Fine-Tuned Model Output

✅ **Valid DOT generated**

```dot
digraph traffic_light {
  rankdir=LR;
  node [shape=circle, style=filled, fontsize=10];
  red [shape=circle, style=filled, fontsize=10, fillcolor=red];
  yellow [shape=circle, style=filled, fontsize=10, fillcolor=yellow];
  green [shape=circle, style=filled, fontsize=10, fillcolor=green];
  green -> red [label="wait"];
  yellow -> green [label="go"];
}
```

![Fine-Tuned Model Graph](showcase/simple_fsm_finetuned.svg)

### Result

🎉 **Fine-tuned model succeeded where base failed!**

---

## Test 2: Workflow

### Prompt

> Generate valid Graphviz DOT code for the described state machine.

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

Task: Design a login workflow state machine with states: LoggedOut, LoggingIn, LoggedIn, and Error. Include transitions for submit, success, failure, and logout.

### Base Model Output

✅ **Valid DOT generated**

```dot
digraph login_workflow {
    StateA [label="Logged Out"];
    StateB [label="Logging In"];
    StateC [label="Logged In"];
    StateD [label="Error"];

    StateA -> StateB [label="Submit Login"];
    StateB -> StateC [label="Enter Username"];
    StateC -> StateD [label="Invalid Username"];

    StateB -> StateD [label="Enter Password"];
    StateD -> StateC [label="Invalid Password"];
    StateC -> StateD [label="Enter Correct Password"];
    StateD -> StateB [label="Login Successful"];

    StateB -> StateA [label="Cancel"];
}
```

![Base Model Graph](showcase/login_flow_base.svg)

### Fine-Tuned Model Output

✅ **Valid DOT generated**

```dot
digraph LoginWorkflow {
	graph [layout=neato]
	node [shape=circle]
	logged_out [shape=rectangle]
	logging_in [shape=rectangle]
	logged_in [shape=rectangle]
	error [shape=rectangle]
	logged_out -> logging_in [label="submit"]
	logging_in -> logged_in [label="submit"]
	logging_in -> error [label="failure"]
	logged_in -> error [label="failure"]
	logged_in -> logged_out [label="logout"]
	error -> logged_in [label="submit"]
	error -> logged_out [label="submit"]
}
```

![Fine-Tuned Model Graph](showcase/login_flow_finetuned.svg)

### Result

✅ **Both models succeeded** - Fine-tuned maintains quality

---

## Test 3: Business Process

### Prompt

> Generate valid Graphviz DOT code for the described state machine.

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

Task: Create a state diagram for order processing: Pending → Processing → Shipped → Delivered. Include a Cancelled state that can be reached from Pending or Processing.

### Base Model Output

✅ **Valid DOT generated**

```dot
digraph order_processing {
    State Pending;
    State Processing;
    State Shipped;
    State Delivered;
    State Cancelled;

    Pending -> Processing;

    Processing -> Delivered;

    Cancelled -> Pending;
    Cancelled -> Processing;
}
```

![Base Model Graph](showcase/order_processing_base.svg)

### Fine-Tuned Model Output

✅ **Valid DOT generated**

```dot
digraph order_states {
  fontname="Helvetica" fontsize=12 penwidth=2.0 splines=true ordering=out compound=true overlap=scale nodesep=0.3 ranksep=0.1
  node [shape=plaintext style=filled fillcolor="#FFFFFF00" fontname=Helvetica fontsize=12 penwidth=2.0]
  edge [fontname=Helvetica fontsize=10]

  "Pending" [shape=circle style=filled class="node large" color=black fillcolor=black fixedsize=true height=0.15 label=""]
  "Processing" [shape=rectangle style=rounded class="node special large" label="processing" color=black fontcolor=black fillcolor=white penwidth=1.0]
  "Processing" -> "Cancelled" [label="cancel\n", color=black class="line"]
  "Cancelled" [shape=circle style=filled class="node large" color=black fillcolor=black fixedsize=true height=0.15 label=""]
  "Shipped" [shape=rectangle style=rounded class="node large" label="shipped" color=black fontcolor=black fillcolor=white penwidth=1.0]
  "Shipped" -> "Processing" [label="ship\n", color=black class="line"]
  "Delivered" [shape=rectangle style=rounded class="node large" label="delivered" color=black fontcolor=black fillcolor=white penwidth=1.0]
  "Delivered" -> "Shipped" [label="deliver\n", color=black class="line"]

}
```

![Fine-Tuned Model Graph](showcase/order_processing_finetuned.svg)

### Result

✅ **Both models succeeded** - Fine-tuned maintains quality

---

## Test 4: Simple FSM

### Prompt

> Generate valid Graphviz DOT code for the described state machine.

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

Task: Model a smart door lock with states: Locked, Unlocked, and Jammed. Include transitions for unlock (Locked→Unlocked), lock (Unlocked→Locked), and jam_detected (any→Jammed).

### Base Model Output

✅ **Valid DOT generated**

```dot
digraph smart_door_lock {
    State Locked -> State Unlocked;
    State Unlocked -> State Locked;

    State Locked -> State Jammed;
    State Unlocked -> State Locked;

    State Locked -> State Unlocked;
    State Jammed -> State Unlocked;
}
```

![Base Model Graph](showcase/door_lock_base.svg)

### Fine-Tuned Model Output

✅ **Valid DOT generated**

```dot
digraph "smart_door_locks" {
  fontname="Helvetica" fontsize=12 penwidth=2.0 splines=true ordering=out compound=true overlap=scale nodesep=0.3 ranksep=0.1
  node [shape=plaintext style=filled fillcolor="#FFFFFF00" fontname=Helvetica fontsize=12 penwidth=2.0]
  edge [fontname=Helvetica fontsize=10]

  "Locked" [margin=0 class="node sealed" label= <
    <table align="center" cellborder="0" border="2" style="rounded" width="48">
      <tr><td width="48" cellpadding="7">Locked</td></tr>
    </table>
  >]
  "Locked" -> "Unlocked" [label="entry_press  \l" class="transition"]
  "Unlocked" [margin=0 class="node" label= <
    <table align="center" cellborder="0" border="2" style="rounded" width="48">
      <tr><td width="48" cellpadding="7">Unlocked</td></tr>
    </table>
  >]
  "Unlocked" -> "Locked" [label="power_off  \l" class="transition"]
  "Locked" -> "Locked" [label= "power_on  \l" class="transition"]
  "Jammed" [margin=0 class="node isolated" label= <
    <table align="center" cellborder="0" border="3" style="rounded" width="48">
      <tr><td width="48" cellpadding="7">Jammed</td></tr>
    </table>
  >]
  "Locked" -> "Jammed" [label="power_off  \l" class="transition"]
  "Jammed" -> "Locked" [label= "power_on  \l" class="transition"]
  "Jammed" -> "Unlocked" [label="power_on  \l" class="transition"]
  "Unlocked" -> "Jammed" [label="door_open  \l" class="transition"]

}
```

![Fine-Tuned Model Graph](showcase/door_lock_finetuned.svg)

### Result

✅ **Both models succeeded** - Fine-tuned maintains quality

---

## Test 5: Complex Workflow

### Prompt

> Generate valid Graphviz DOT code for the described state machine.

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

Task: Payment processing state machine: Initiated → Authorizing → Authorized → Capturing → Completed. Include Failed state reachable from Authorizing and Capturing.

### Base Model Output

✅ **Valid DOT generated**

```dot
digraph PaymentProcessingStateMachine {
  State Initiated -> State Authorizing;
  State Authorizing -> State Processing;
  State Processing -> State Authorized;
  State Authorized -> State Capturing;
  State Capturing -> State Completed;
  State Authorizing -> State Failed;
  State Capturing -> State Failed;
  State Failed -> State Initiated;
}
```

![Base Model Graph](showcase/payment_gateway_base.svg)

### Fine-Tuned Model Output

❌ **Failed to generate valid DOT**

<details>
<summary>Raw output (click to expand)</summary>

```
digraph PaymentProcessing {
  fontname="Helvetica" fontsize=12 penwidth=2.0 splines=true ordering=out compound=true overlap=scale nodesep=0.3 ranksep=0.1
  node [shape=plaintext style=filled fillcolor="#FFFFFF00" fontname=Helvetica fontsize=12 penwidth=2.0]
  edge [fontname=Helvetica fontsize=10]

  "Initiated" [shape=circle style=filled class="state initial" color="black" fillcolor="black" fixedsize=true height=0.15 label=""]
  "Initiated" -> "Authorizing" [label="trigger \$amount >= \$min_amount\nget_authorization_approval\nenabled\nexit\nsome_approval_process\nsome_approval_process\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t" style=dashed color="#0E1D1E" width=0.1]
  "Authorizing" [margin=0 class="state authorized" label= ""]
  "Authorizing" -> "Authorized" [label="trigger \$amount >= \$min_amount\nuser_approval_granted\npayment_authorized\nexit\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t" style=rounded penwidth=4.0]
  "Authorized" [shape=circle style=filled class="state authorized" color="black" fillcolor="black" fixedsize=true height=0.15 label=""]
  "Authorized" -> "Capturing" [label="
```

</details>

### Result

⚠️ **Regression** - Base succeeded but fine-tuned failed

---

## Test 6: Business Process

### Prompt

> Generate valid Graphviz DOT code for the described state machine.

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

Task: Document approval workflow: Draft → Review → Approved/Rejected. From Rejected, can go back to Draft for revision.

### Base Model Output

❌ **Failed to generate valid DOT**

<details>
<summary>Raw output (click to expand)</summary>

```
```dot
digraph approval_workflow {
    StateStart --> Draft;
    Draft --> Review;
    Review --> Approved;
    Review --> Rejected;
    Rejected --> Draft;
}
```
```

</details>

### Fine-Tuned Model Output

✅ **Valid DOT generated**

```dot
digraph approval_workflow {
  fontname="Helvetica" fontsize=12 penwidth=2.0 splines=true ordering=out compound=true overlap=scale nodesep=0.3 ranksep=0.1
  node [shape=plaintext style=filled fillcolor="#FFFFFF00" fontname=Helvetica fontsize=12 penwidth=2.0]
  edge [fontname=Helvetica fontsize=10]

  "Original Draft" [shape=circle fixedsize=true width=0.15 height=0.15 fixedcolor=true color="black" fillstyle=filled]
  "Original Draft" -> "Review" [label="    \l" color=black fontcolor=black fillstyle=empty]
  "Review" [shape=circle fixedsize=true width=0.15 height=0.15 fixedcolor=true color="black" fillstyle=filled]
  "Review" -> "Approved" [label="    \l" color=black fontcolor=black fillstyle=empty]
  "Approved" [shape=circle fixedsize=true width=0.15 height=0.15 fixedcolor=true color="black" fillstyle=filled]
  "Approved" -> "Reviewed" [label="    \l" color=black fontcolor=black fillstyle=empty]
  "Reviewed" [shape=circle fixedsize=true width=0.15 height=0.15 fixedcolor=true color="black" fillstyle=empty]
  "Reviewed" -> "Draft" [label="    \l" color=black fontcolor=black fillstyle=empty]
  "Rejected" [shape=circle fixedsize=true width=0.15 height=0.15 fixedcolor=true color="black" fillstyle=empty]
  "Rejected" -> "Draft" [label="    \l" color=black fontcolor=black fillstyle=empty]
}
```

![Fine-Tuned Model Graph](showcase/document_approval_finetuned.svg)

### Result

🎉 **Fine-tuned model succeeded where base failed!**

---

## Test 7: Device Control

### Prompt

> Generate valid Graphviz DOT code for the described state machine.

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

Task: Media player state machine with states: Stopped, Playing, Paused. Include transitions: play, pause, stop, resume.

### Base Model Output

✅ **Valid DOT generated**

```dot
digraph media_player_state_machine {
  State Stopped -> State Playing;
  State Playing -> State Pausing;
  State Pausing -> State Stopped;
  State Stopped -> State Resume;
  State Playing -> State Stopped;
  State Pausing -> State Playing;
  State Resume -> State Playing;
}
```

![Base Model Graph](showcase/media_player_base.svg)

### Fine-Tuned Model Output

✅ **Valid DOT generated**

```dot
digraph media_player_state_machine {
  fontname="Helvetica" fontsize=12 penwidth=2.0 splines=true ordering=out compound=true overlap=scale nodesep=0.3 ranksep=0.1
  node [shape=plaintext style=filled fillcolor="#FFFFFF00" fontname=Helvetica fontsize=12 penwidth=2.0]
  edge [fontname=Helvetica fontsize=10]

  "Stopped" [margin=0 class="state stopped" label= <
    <table align="center" cellborder="0" border="2" style="rounded" width="48">
      <tr><td width="48" cellpadding="7">Stopped</td></tr>
    </table>
  >]
  "Playing" [margin=0 class="state playing" label= <
    <table align="center" cellborder="0" border="2" style="rounded" width="48">
      <tr><td width="48" cellpadding="7">Playing</td></tr>
    </table>
  >]
  "Paused" [margin=0 class="state paused" label= <
    <table align="center" cellborder="0" border="2" style="rounded" width="48">
      <tr><td width="48" cellpadding="7">Paused</td></tr>
    </table>
  >]
  "resume" [shape=rect style=filled class="state playable" color="black" fillcolor="black" width="1" height="1" label=""]
  "play" [shape=rect style=rounded class="state playable" color="black" fillcolor="none" fixedsize=true height=1.5 label=""]
  "pause" [shape=rect style=rounded class="state playable" color="black" fillcolor="none" fixedsize=true height=1.5 label=""]
  "stop" [shape=rect style=rounded class="state playable" color="black" fillcolor="none" fixedsize=true height=1.5 label=""]

}
```

![Fine-Tuned Model Graph](showcase/media_player_finetuned.svg)

### Result

✅ **Both models succeeded** - Fine-tuned maintains quality

---

## Test 8: Network Protocol

### Prompt

> Generate valid Graphviz DOT code for the described state machine.

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

Task: TCP connection states: Closed → SynSent → Established → FinWait → Closed. Show the connection lifecycle.

### Base Model Output

✅ **Valid DOT generated**

```dot
digraph TCP_connection_states {
  State_Closed -> State_SynSent;
  State_SynSent -> State_Established;
  State_Established -> State_FinWait;
  State_FinWait -> State_Closed;
}
```

![Base Model Graph](showcase/network_connection_base.svg)

### Fine-Tuned Model Output

✅ **Valid DOT generated**

```dot
digraph tcp_connection_states {
  fontname="Helvetica" fontsize=12 penwidth=2.0 splines=true ordering=out compound=true overlap=scale nodesep=0.3 ranksep=0.1
  node [shape=circle style=filled fillcolor="#FFFFFF00" fixedsize=true defaultsize=1000000 name=str labeldose=2 shape=rect style=filled class="ipnode" color="#FFFFFF00" penwidth=2.0]
  edge [fontname=Helvetica fontsize=10]

  "CLOSED" [shape=circle style=filled class="ipnode" color="#FFFFFF00" fixedsize=true defaultsize=100 iflabel=check labeldose=1 align=center penwidth=1.0]
  "CLOSED" -> "SYN_SENT" [label="arrow   \l" class="running"]
  "SYN_SENT" [margin=0 class="ipnode" label=" " shape=circle style=filled class="ipnode" fixedsize=true defaultsize=100 iflabel=check labeldose=1 align=center penwidth=1.0]
  "SYN_SENT" -> "ESTABLISHED" [label="arrow   \l" class="running"]
  "ESTABLISHED" [margin=0 class="ipnode" label=" " shape=circle style=filled class="ipnode" fixedsize=true defaultsize=100 iflabel=check labeldose=1 align=center penwidth=1.0]
  "ESTABLISHED" -> "FIN_WAIT" [label="arrow   \l" class="running"]
  "FIN_WAIT" [margin=0 class="ipnode" label=" " shape=circle style=filled class="ipnode" fixedsize=true defaultsize=100 iflabel=check labeldose=1 align=center penwidth=1.0]
  "FIN_WAIT" -> "CLOSED" [label="arrow   \l" class="running"]

}
```

![Fine-Tuned Model Graph](showcase/network_connection_finetuned.svg)

### Result

✅ **Both models succeeded** - Fine-tuned maintains quality

---

