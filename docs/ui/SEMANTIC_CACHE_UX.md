# Antigravity Semantic Cache UX

Antigravity uses semantic caching to save cost and time by reusing previously generated reasoning and artifacts. This document defines the visibility of this feature.

## 1. Cache Hit Indicators
- **The "Lightning" Icon**: A small icon next to trace entries or artifacts that were retrieved from the cache.
- **"Saved by Cache" Badge**: Showing the time and tokens saved for a specific task step.
  - *Example*: `[Cached] Saved 2,400 tokens and 12 seconds.`

## 2. Cached Reasoning Trace
- **Trace Origin**: When a reasoning block is cached, the UI provides a link to the "Original Task" that generated it.
- **Confidence of Match**: A score (0-100%) showing how semantically similar the current goal is to the cached entry.

## 3. Cache Management for Operators
- **"Refresh" Action**: Allow users to bypass the cache and force the agent to "Re-think" a step from scratch.
- **Cache Explorer**: A view to browse successfully cached patterns and their usage frequency across the organization.

## 4. Organization-wide Intelligence
- **Knowledge Sharing**: Highlight when an agent is using a pattern learned from a *different* user (if authorized by privacy policy).
- **Common Logic Nodes**: Visualization of "High-Traffic" reasoning paths that are frequently serving the team from the cache.

## 5. Security of the Cache
- **Stale Data Warning**: If the cached data is more than X days old, the UI flags it: "Using cached logic from 30 days ago. Refresh suggested."
- **Privacy Gating**: Ensure that cached artifacts containing PII are never served to unauthorized users, even if the semantic goal matches.
