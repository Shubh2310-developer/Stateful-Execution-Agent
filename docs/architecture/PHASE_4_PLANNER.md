# Phase 4: The Planner System

This phase implements the strategic "brain" of the agent, responsible for decomposing complex goals into a structured, executable sequence of steps.

## Goals
- Implement the goal parsing and decomposition logic.
- Create a step generator that respects dependencies and tool availability.
- Implement a plan validation engine to ensure completeness.
- Integrate memory retrieval into the planning process for strategic learning.

## 4.1 Goal Parsing (`src/planner/goal_parser.py`)
- **Implementation**:
    - Extract entities, constraints, and implicit requirements from unstructured user input.
    - Identify required output formats and deadlines.
    - Map the goal to high-level capabilities (e.g., Search, Analysis, Synthesis).

## 4.2 Step Generation (`src/planner/step_generator.py`)
- **Prompt Strategy**: Use a chain-of-thought system prompt that forces the LLM to think about dependencies before listing steps.
- **Constraints**:
    - Atomic steps: One responsibility per step.
    - Linear vs. Directed Acyclic Graph (DAG) support: Steps must have clear `dependencies` fields.
    - Tool Assignment: Automatically match step requirements to available tools from the registry.

## 4.3 Dependency Analysis (`src/planner/dependency_analyzer.py`)
- **Implementation**:
    - Topological sort of generated steps.
    - Detection of circular dependencies.
    - Validation that required inputs for Step N are produced by Step N-X.

## 4.4 Plan Validation (`src/planner/plan_validator.py`)
- **Implementation**:
    - A secondary LLM call (or a rule-based engine) to review the plan.
    - Checks for:
        - Goal coverage: Does this plan actually achieve the user's intent?
        - Feasibility: Are the estimated durations realistic?
        - Security: Are there any risky actions being planned without approval?

## 4.5 Adaptive Planning Integration
- **Mechanism**:
    - Query long-term memory for similar past goals during the planning phase.
    - Inject "Lessons Learned" from memory into the planning prompt (e.g., "In the past, the user preferred X format for this type of task").

## Verification Criteria
- [ ] Planner takes a complex goal and outputs a structured JSON plan with at least 3 dependent steps.
- [ ] Steps correctly reference required tools.
- [ ] Dependency analyzer correctly identifies an out-of-order plan.
- [ ] Plan validator flags a plan that misses a key part of the user's request.
