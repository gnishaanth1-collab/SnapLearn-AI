# UML

## Use Case
Student -> Login/Register
Student -> Upload Material
Student -> Summarize
Student -> Ask AI
Student -> Generate Quiz
Student -> Flashcards
Student -> Study Plan
Student -> Analytics
Student -> Export Report
Student -> Snapdragon Diagnostics

## Component
PySide6 UI -> Application Services -> Document Service
Application Services -> Local Retrieval -> Optional Local LLM
Application Services -> Qualcomm AI Hub / ONNX / QNN adapter
All local data -> SQLite

## Activity
Upload -> Extract -> Chunk -> Retrieve -> Generate/Answer -> Display -> Save results
