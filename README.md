# SnapLearn AI

A complete runnable college-project prototype for an on-device personalized learning
assistant optimized for Snapdragon-powered HP PCs.

## Features
- Login/register
- PDF/DOCX/PPTX/TXT import
- Local document library
- AI summarization
- Document-grounded Q&A
- Optional local Ollama generation
- Quiz generation/scoring
- Flashcards
- Personalized study planner
- Learning analytics
- PDF report
- Snapdragon/AI Hub diagnostics and ONNX benchmark
- Documentation for Qualcomm AI Hub optimization

## Run on Windows
1. Install Python 3.11+.
2. Open Command Prompt in this folder.
3. `python -m venv .venv`
4. `.\.venv\Scriptsctivate`
5. `pip install -r requirements.txt`
6. `python main.py`

Demo:
Email: student@snaplearn.local
Password: student123

For native Snapdragon Windows, use ARM64 Python when possible. See
docs/SNAPDRAGON_OPTIMIZATION.md for the Qualcomm AI Hub stage.

The baseline app works without an AI API key. Optional local generation uses Ollama.
