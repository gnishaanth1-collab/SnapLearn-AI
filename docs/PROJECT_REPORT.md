# SnapLearn AI - Project Report

## Abstract
SnapLearn AI is a privacy-oriented personalized learning assistant designed for
Snapdragon-powered HP Windows PCs. It converts student documents into summaries,
document-grounded answers, quizzes, flashcards, study plans and learning analytics.

## Problem
Students work with long PDFs, slides and notes and spend time searching manually.
Cloud AI can also be undesirable for private educational material.

## Objectives
- Process learning documents locally.
- Generate concise study resources.
- Provide document-grounded Q&A.
- Generate quizzes and flashcards.
- Build adaptive study plans.
- Track learning performance.
- Integrate Qualcomm AI Hub optimized models.
- Measure Snapdragon execution performance.

## Modules
Authentication, document management, summarization, retrieval Q&A, quiz engine,
flashcards, planner, analytics, PDF reporting and Snapdragon diagnostics.

## Innovation
The architecture is local-first and separates retrieval from model generation, making
it possible to replace the local fallback generator with a Qualcomm AI Hub optimized
model without redesigning the UI.

## Limitation
The exact NPU runtime/model artifact is device-specific. Final challenge evidence must
be captured on the actual HP Snapdragon PC.

## Future Scope
Voice tutoring, OCR, multilingual tutoring, richer adaptive learning and a bundled
AI Hub model.
