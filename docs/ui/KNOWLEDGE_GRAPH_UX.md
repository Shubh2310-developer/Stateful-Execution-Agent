# Antigravity Knowledge Graph UX

The Knowledge Graph is the visual representation of the agent's long-term memory, showing the interconnected nature of learned facts, preferences, and domain knowledge.

## 1. Graph Visualization (The Memory Map)
- **Nodes**: Represent atomic pieces of knowledge (e.g., "User Role," "Preferred Tone," "Financial KPI Definition").
- **Edges**: Represent relationships (e.g., "Influences," "Defined By," "Contradicts").
- **Clustering**: Nodes are automatically grouped into "Semantic Islands" (e.g., a cluster of nodes related to "Project X").

## 2. Interactive Discovery
- **Zoom & Explore**: An infinite canvas (e.g., React Flow or D3-force) where users can zoom in on specific clusters.
- **Node Preview**: Click a node to open a sidebar with the full detail of the memory entry, its source task, and its confidence score.
- **Search & Focus**: Use the global search to find a specific node and "Fly" the camera to its location in the graph.

## 3. Editing via Graph
- **Manual Association**: Allow users to drag lines between nodes to manually define relationships.
- **Pruning**: A specialized "Scissors" tool to cut incorrect associations.
- **Merging**: Drag two nodes onto each other to "De-duplicate" or merge similar concepts.

## 4. Influence Paths
When viewing a specific Decision Trace entry, show a "Memory Path" — a visual overlay on the graph showing the chain of nodes that influenced that specific reasoning.

## 5. Visual Standards
- **Node Styling**:
  - **Confidence**: Node size or border thickness reflects the agent's confidence.
  - **Recency**: Node brightness or color saturation reflects how recently the memory was used.
  - **Category**: Use a consistent color palette for different types of knowledge (e.g., Preferences = Blue, Domain Facts = Emerald).
- **Edge Styling**:
  - **Directionality**: Use arrows to show the direction of influence.
  - **Strength**: Line weight reflects the strength of the association.
