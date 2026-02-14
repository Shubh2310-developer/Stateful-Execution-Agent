# Phase 9: Review, Feedback & Optimization

This final phase focuses on the quality assurance loop, allowing the agent to validate its own work and learn from user feedback.

## Goals
- Implement the Reviewer module.
- Build the Success Validation engine.
- Create the Feedback Processing loop.
- Implement final quality checks and project-wide optimization.

## 9.1 The Reviewer (`src/reviewer/reviewer.py`)
- **Implementation**:
    - A dedicated agent personality that takes the completed artifacts and the original goal.
    - "Self-Correction" loop: If the Reviewer finds flaws, it sends the task back to the Executor with specific revision instructions.

## 9.2 Quality Checker (`src/reviewer/quality_checker.py`)
- **Implementation**:
    - Non-LLM checks: File existence, word counts, valid JSON/PDF formats.
    - LLM-powered checks: Tone consistency, requirement coverage, accuracy of facts.

## 9.3 Feedback Processor (`src/memory/learning/feedback_processor.py`)
- **Implementation**:
    - Logic to parse user ratings (1-5) and text feedback.
    - Correlation analysis: Linking feedback to specific steps or decisions in the trace.
    - Update the `HistoricalPatterns` and `UserPreferences` in long-term memory based on the feedback.

## 9.4 Success Validation (`src/reviewer/success_validator.py`)
- **Implementation**:
    - Compare final output against the `parsed_goal.success_criteria` defined in Phase 4.
    - Generate a "Completion Report" summarizing what was achieved and any caveats.

## 9.5 System Optimization
- **Implementation**:
    - Prompt Tuning: Refining system prompts based on common failure modes discovered during testing.
    - Model Selection Optimization: Logic to use cheaper models (Haiku/Flash) for simple tasks and more powerful models (Opus/Sonnet) for complex planning/review.
    - Caching Layer: Implementing Redis caching for repetitive retrieval queries.

## Verification Criteria
- [ ] Reviewer correctly identifies a missing requirement in a test task.
- [ ] User feedback (e.g., "Make it shorter") correctly updates the user's preference profile.
- [ ] Final task status is only set to "COMPLETED" after a successful Reviewer pass.
- [ ] System accurately reports a `QualityScore` for the final output.
