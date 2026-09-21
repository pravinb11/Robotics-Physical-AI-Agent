# Physical AI Agent

A stateful **Physical AI agent** that converts natural-language commands into robot actions using **LLM reasoning, world-state representation, perception, tool calling, and closed-loop execution**.

The project explores how foundation models can act as the high-level intelligence of a robot while classical robotics systems handle physical execution.

---

## Overview

A conventional robot typically requires explicitly programmed task logic:

```text
User Command
     ↓
Hard-coded Task Logic
     ↓
Robot Skills
     ↓
Robot
```

This project introduces an AI reasoning layer:

```text
                ┌──────────────────────┐
                │     User Command     │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │      LLM Reasoner    │
                │   Task Understanding │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │    Tool / Skill      │
                │      Selection       │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │    Tool Executor     │
                │  Validation / Safety │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │     World State      │
                │ Robot + Objects +    │
                │ Environment State    │
                └──────────┬───────────┘
                           ↓
                    Feedback to LLM
```

The central idea is:

> **The LLM decides what the robot should do; the execution layer determines whether and how that action can actually be performed.**

---

# Current Capability

The current prototype supports language-conditioned object retrieval in a simulated/mock environment.

Example:

```text
User:
Bring the red bottle
```

The agent can reason over the available world state and generate actions such as:

```text
navigate(kitchen)
        ↓
grasp(red_bottle)
        ↓
place(red_bottle, living_room)
```

Each action is executed through a tool interface and the resulting state is fed back into the agent.

---

# Key Features

### 🧠 LLM-based Task Reasoning

Uses an LLM as the high-level reasoning layer for interpreting natural-language commands and selecting robot skills.

### 🌎 Explicit World State

The robot maintains a structured representation of:

* Robot location
* Robot position
* Currently held object
* Objects in the environment
* Object locations
* Object visibility
* Object graspability
* People and their locations

Example:

```python
{
    "robot": {
        "location": "living_room",
        "position": [0.0, 0.0, 0.0],
        "holding": None
    },
    "objects": {
        "red_bottle": {
            "type": "bottle",
            "location": "kitchen",
            "visible": True,
            "graspable": True
        }
    }
}
```

### 🔧 Tool Calling

The LLM interacts with the robot through structured tools:

```text
navigate()
detect()
grasp()
place()
```

This creates a clean interface between AI reasoning and robot execution.

### 🔄 Closed-Loop Execution

The agent does not simply generate an entire plan and execute it blindly.

Instead:

```text
LLM
 ↓
Tool Call
 ↓
Execution
 ↓
Tool Result
 ↓
World State Update
 ↓
LLM
 ↓
Next Action
```

This allows the robot to react to the result of previous actions.

### 🛡️ Execution Validation

The execution layer validates tool requests against the current world state.

For example, if the LLM attempts:

```text
grasp(apple)
```

while no `apple` exists in the world:

```text
FAILED
reason: Unknown object: apple
```

The executor therefore acts as a boundary between probabilistic language reasoning and deterministic robot execution.

---

# Architecture

```text
                    USER
                     │
                     ▼
             ┌───────────────┐
             │  LLM Reasoner │
             └───────┬───────┘
                     │
              Function Calls
                     │
                     ▼
             ┌───────────────┐
             │ Tool Executor │
             └───────┬───────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Navigate     Detect     Grasp
          │          │          │
          └──────────┼──────────┘
                     ▼
                  Place
                     │
                     ▼
             ┌───────────────┐
             │  World State  │
             └───────┬───────┘
                     │
                     │ Feedback
                     ▼
             ┌───────────────┐
             │ LLM Reasoner  │
             └───────────────┘
```

---

# Project Structure

```text
physical-ai-agent/
│
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── llm.py
│   └── planner.py
│
├── execution/
│   ├── __init__.py
│   └── tool_executor.py
│
├── perception/
│   ├── __init__.py
│   └── mock_perception.py
│
├── skills/
│   ├── __init__.py
│   ├── navigate.py
│   ├── detect.py
│   ├── grasp.py
│   └── place.py
│
├── world/
│   ├── __init__.py
│   ├── object.py
│   ├── scene_graph.py
│   └── world_state.py
│
├── tests/
│   ├── test_skills.py
│   ├── test_world.py
│   ├── test_perception.py
│   ├── test_scene_graph.py
│   └── test_gemini.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/physical-ai-agent.git
cd physical-ai-agent
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

The project currently uses Google's Gemini Python SDK:

```text
google-genai
```

---

# Configuration

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Verify:

```bash
echo "${GEMINI_API_KEY:+GEMINI_API_KEY loaded}"
```

Expected:

```text
GEMINI_API_KEY loaded
```

> Never commit your API key to GitHub.

---

# Running the Agent

Start the agent:

```bash
python3 main.py
```

Example:

```text
Robot command: Bring the red bottle
```

The agent receives the command and reasons over the current world.

Example execution:

```text
AGENT STEP 1
[LLM TOOL CALL] navigate
[ARGUMENTS] {'target': 'kitchen'}

[NAVIGATE] Going to kitchen

[TOOL RESULT]
{'status': 'SUCCESS',
 'skill': 'navigate',
 'target': 'kitchen'}
```

The world state is then updated before the next reasoning step.

---

# Example World

The current mock perception system initializes the environment with:

```text
Living Room
│
├── Robot
└── User

Kitchen
│
├── Red Bottle
└── Blue Cup

Office
│
└── Laptop
```

The robot initially starts in:

```text
living_room
```

Available objects:

| Object       | Type   | Location | Graspable |
| ------------ | ------ | -------- | --------- |
| `red_bottle` | bottle | kitchen  | Yes       |
| `blue_cup`   | cup    | kitchen  | Yes       |
| `laptop`     | laptop | office   | Yes       |

---

# Design Principles

## 1. World State is the Source of Truth

The LLM should not invent physical objects or locations.

Bad:

```text
User: Bring the red bottle

LLM: I'll get the apple.
```

The execution layer prevents this by validating requested objects against the world state.

---

## 2. LLM Does Not Directly Control the Robot

The LLM produces structured actions:

```text
navigate(...)
grasp(...)
place(...)
```

The executor decides whether those actions are valid.

This separation is important because LLMs are probabilistic while robot execution requires deterministic safety constraints.

---

## 3. Closed-Loop Rather Than Open-Loop Planning

Instead of:

```text
LLM → complete plan → execute blindly
```

the system uses:

```text
LLM
 ↓
Action
 ↓
Execution
 ↓
Observation
 ↓
World State Update
 ↓
LLM
```

This enables future integration with real perception and robot feedback.

---

# Current Limitations

This repository is currently a prototype.

The present implementation uses:

* Mock perception
* Simulated robot skills
* Simplified world state
* LLM-based reasoning
* Deterministic tool execution

It does **not yet** provide:

* Real camera perception
* VLM-based visual grounding
* Real object detection
* Real manipulation
* ROS2 integration
* Navigation stack integration
* G1 hardware integration
* VLA policies
* Reinforcement-learning-based skills

These are planned extensions.

---

# Roadmap

## Phase 1 — Agent Foundation

* [x] LLM task reasoning
* [x] Structured tool calling
* [x] World-state representation
* [x] Mock perception
* [x] Tool execution layer
* [x] Execution validation
* [x] Closed-loop tool execution
* [ ] Physically consistent tool validation
* [ ] Scene graph integration
* [ ] Robust task planner

## Phase 2 — Perception

* [ ] Camera input
* [ ] Object detection
* [ ] Object tracking
* [ ] Visual grounding
* [ ] VLM integration
* [ ] Real-time world-state updates

## Phase 3 — Robot Integration

* [ ] ROS2 interface
* [ ] Navigation skill
* [ ] Manipulation skill
* [ ] Grasp planning
* [ ] Nav2 integration
* [ ] Robot execution monitoring

## Phase 4 — Humanoid Integration

Target platform:

**Unitree G1**

```text
Physical AI Agent
        │
        ▼
Task Planner
        │
        ▼
Robot Skills
        │
        ├── Navigation
        ├── Whole Body Control
        ├── Locomotion
        └── Manipulation
                │
                ▼
              G1
```

Existing robotics components such as ROS2, Nav2, motion control, WBC/MPC, and low-level controllers can serve as the execution layer.

## Phase 5 — Learned Physical Intelligence

* [ ] Imitation Learning
* [ ] Reinforcement Learning
* [ ] Vision-based RL
* [ ] Vision-Language-Action models
* [ ] Skill learning
* [ ] Long-horizon task execution
* [ ] Sim-to-real transfer

---

# Research Direction

The longer-term goal is to investigate a modular Physical AI architecture combining:

```text
Language
   +
Vision
   +
World Modeling
   +
Reasoning
   +
Task Planning
   +
Learned Skills
   +
Classical Robot Control
```

The project is designed around a key principle:

> **Foundation models provide semantic reasoning and task-level intelligence, while classical robotics provides reliable physical execution.**

---

# Technologies

* Python
* Google Gemini
* LLM Tool Calling
* Object-Centric World State
* Function Calling
* Robot Skill APIs
* ROS2 *(planned)*
* Nav2 *(planned)*
* VLM *(planned)*
* VLA *(planned)*
* Reinforcement Learning *(planned)*
* Unitree G1 *(planned)*

---

# Author

**Pravin Behera**

PhD — Control Systems, IIT Kharagpur

Research interests:

* Physical AI
* Humanoid Robotics
* Robot Learning
* Reinforcement Learning
* Motion Planning
* Robot Control
* Negative-Imaginary Systems
* Embodied AI
* Vision-Language-Action Models

---

# License

This project is intended for research, experimentation, and educational purposes.

Add a specific open-source license here if/when the repository is released under one.
