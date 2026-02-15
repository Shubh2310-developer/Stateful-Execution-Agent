# Antigravity Knowledge Base Management UX

The Knowledge Base is the agent's "Source of Truth" for domain-specific information. This document defines the patterns for curating and monitoring these datasets.

## 1. Source Curation
- **Document Hub**: A searchable list of all files, web pages, and API sources available to the agent.
- **Indexing Status**: Real-time progress bars for document embedding and vectorization.
- **Source Health**: Indicators showing if a remote source (e.g., a Confluence page) is currently reachable.

## 2. Semantic Search Preview
- **"What does the Agent see?"**: A testing tool where users enter a query and see the top 5 chunks of text retrieved from the knowledge base.
- **Relevance Tuning**: A UI for adjusting the weighting of different sources (e.g., "Prioritize the 2024 Product Roadmap over 2023 docs").

## 3. Knowledge Conflict Resolution
- **Contradiction Finder**: The agent flags when two sources provide conflicting information.
- **Human Arbiter UI**: A side-by-side view where a user selects which source is the "Truth" or provides a manual correction.

## 4. Active Knowledge Injection
- **Flash Context**: A way to upload a temporary file for a single task without committing it to the global knowledge base.
- **Quick-add Snippets**: A text field for adding "Sticky Notes" of tribal knowledge that isn't documented elsewhere.

## 5. Knowledge Graph Integration
- **Contextual Visualization**: Links back to the [Knowledge Graph](./KNOWLEDGE_GRAPH_UX.md) to show how a specific source has been "Atomized" into learned facts.
