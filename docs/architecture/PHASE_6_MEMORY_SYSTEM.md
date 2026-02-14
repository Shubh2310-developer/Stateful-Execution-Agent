# Phase 6: Memory Architecture

This phase implements the "learning" capability of the agent, allowing it to remember user preferences and adapt its behavior over time.

## Goals
- Implement task-scoped Short-Term Memory.
- Build the User-scoped Long-Term Memory store.
- Implement semantic retrieval for historical patterns.
- Create the learning loop to update memory after task completion.

## 6.1 Short-Term Memory (`src/memory/short_term/task_context.py`)
- **Implementation**:
    - Ephemeral context store for the current task.
    - Working variables (e.g., intermediate numbers, temporary strings).
    - Logic to prioritize what context to keep when the prompt window is nearly full.

## 6.2 Long-Term Memory Store (`src/memory/long_term/`)
- **User Profile**: Persistent facts about the user (Role, Preferences, Style).
- **Domain Knowledge**: Facts learned about the specific industry or project.
- **Historical Patterns**: Structured records of past tasks, plans, and success scores.

## 6.3 Retrieval Engine (`src/memory/retrieval/semantic_search.py`)
- **Library**: `Sentence-Transformers` or `OpenAI Embeddings`.
- **Implementation**:
    - Vectorize past task descriptions and reasoning traces.
    - Store in a vector database (e.g., ChromaDB, Qdrant, or MongoDB Vector Search).
    - Logic to find "Top K" relevant experiences for a new goal.

## 6.4 Learning Loop (`src/memory/learning/adaptation_engine.py`)
- **Trigger**: Task completion or user feedback.
- **Implementation**:
    - LLM-powered extraction: "What did we learn from this task?"
    - Pattern identification: Did we use a successful new structure?
    - Update preferences: Did the user correct our tone?
    - Commit to long-term memory.

## 6.5 Context Builder (`src/memory/retrieval/context_builder.py`)
- **Implementation**:
    - Logic to select the most relevant pieces of memory for a given prompt.
    - Ranking algorithm to balance "Most Recent" vs "Most Relevant" vs "Always Include" (Pinned) memories.

## Verification Criteria
- [ ] Successfully retrieve relevant "User Preferences" during a test prompt.
- [ ] Task completion triggers an update to the "Historical Patterns" collection.
- [ ] Semantic search finds a similar task from a pool of 100 dummy records.
- [ ] Short-term memory successfully manages variables across multiple steps.
