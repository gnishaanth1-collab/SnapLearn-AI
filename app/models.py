from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    question: str
    options: List[str]
    answer: int
    explanation: str = ""
