import re
from .ai_service import sentences
from app.models import Question

def generate_quiz(text, count=5):
    ss = sentences(text)
    questions = []
    for s in ss:
        m = re.search(r'\b([A-Za-z][A-Za-z0-9-]{3,})\b', s)
        if not m:
            continue
        answer_word = m.group(1)
        blank = re.sub(r'\b' + re.escape(answer_word) + r'\b', "_____", s, count=1, flags=re.I)
        distractors = []
        for other in ss:
            mm = re.search(r'\b([A-Za-z][A-Za-z0-9-]{3,})\b', other)
            if mm and mm.group(1).lower() != answer_word.lower():
                distractors.append(mm.group(1))
            if len(distractors) >= 3:
                break
        opts = [answer_word] + distractors[:3]
        while len(opts) < 4:
            opts.append("None of the above")
        questions.append(Question(blank, opts, 0, s))
        if len(questions) >= count:
            break
    return questions
