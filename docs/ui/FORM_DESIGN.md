# Antigravity Form & Input UX

Forms in Antigravity are used for goal initiation, tool configuration, and feedback. This document defines the standards for data entry and configuration.

## 1. Input Field Design
- **Style**: Clear borders (`border-slate-300`), focus states (`ring-2 ring-blue-500`), and rounded corners (`rounded-lg`).
- **Typography**: `text-base` (16px) for mobile accessibility, `text-sm` for high-density desktop views.
- **Labels**: Always visible, positioned above the input. Never rely on placeholders as the only label.

## 2. The "New Task" Experience
The most critical form in the application.
- **NLP-First**: A large, multi-line text area optimized for natural language goals.
- **Smart Completion**: Suggest common goals or templates based on user history as they type.
- **Constraint Tags**: Allow users to quickly add parameters like `--deadline:tomorrow` or `--format:pdf` which turn into visual chips.

## 3. Feedback & Correction Inputs
- **Inline Refinement**: Small, context-aware inputs that appear directly next to the artifact or trace entry being corrected.
- **Sentiment Indicators**: Subtle visual cues (e.g., color-coded borders) that reflect the "Tone" the user is employing, which the agent uses to adjust its voice.

## 4. Validation & Error Handling
- **Real-time Validation**: Check for missing required fields or invalid formats (e.g., malformed API keys) as the user types.
- **Clear Error Messages**: Positioned directly below the affected input in red text (`text-red-600`).
- **Success States**: Subtle green border/check icon when a complex input (like a database connection string) is successfully verified.

## 5. Multi-step Configuration (Steppers)
For complex setup (e.g., connecting a new enterprise tool):
- **Progress Indicator**: A top-level stepper showing "Connection -> Permissions -> Test -> Save."
- **Draft Persistence**: Automatically save form state so users can leave and return without losing their configuration.
- **"Save & Test"**: Always provide a way to verify a connection before finalizing the form.
