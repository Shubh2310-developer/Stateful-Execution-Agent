# Antigravity Feedback & Learning UI

The Feedback system is the bridge between a completed task and the agent's long-term intelligence. This document defines the post-execution optimization loop.

## 1. Post-Task Feedback Card
Presented immediately after a task reaches the "Completed" status.

- **Star Rating (1-5)**: Quick, quantitative assessment of quality.
- **Specific Success Checklist**: Users can check which of the original goal's success criteria were actually met.
- **Open Feedback**: A text area for nuanced adjustments (e.g., "The metrics were perfect, but the tone was too informal").

## 2. The Learning Impact Summary
After feedback is submitted, the UI shows what the agent "learned."

- **Learned Facts**: "Saved: You prefer reports under 1000 words."
- **Trend Update**: "Your satisfaction with 'Investor Updates' has improved by 12%."
- **Preference Toggle**: Allow the user to "Confirm" or "Discard" a piece of learned knowledge immediately.

## 3. Iterative Refinement Request
If the user is not satisfied:

- **"Try Again" CTA**: Restarts the planning phase with the feedback as a new constraint.
- **Incremental Improvement**: The agent suggests 3 ways it could improve the result based on the feedback.
- **Comparison View**: Show the "Bad" version next to the "Corrected" version during the refinement process.

## 4. Global Preference Dashboard
Where all feedback-driven learning is aggregated.

- **Learning Timeline**: A log of when specific preferences were learned and which tasks influenced them.
- **Manual Overrides**: The user can "Pin" certain rules to ensure they are never overwritten by future learning.

## 5. Emotional/Sentiment Awareness
- **Tone Detection**: The agent can use the user's feedback tone to adjust its future communication style (e.g., if feedback is consistently concise, the agent becomes more concise).
- **Proactive Apology**: If a task fails or receives a 1-star rating, the agent acknowledges the failure in the next session and asks for specific guidance.
