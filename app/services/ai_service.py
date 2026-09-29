import re
import requests
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .document_service import chunk_text

STOP = set("the a an and or of to in is are was were for with on as by from that this these those it its be been being at into about than then them they their you your we our can could should would may might will shall has have had do does did not no yes very more most some any each also only using used use".split())

def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 30]

def summarize(text, max_sentences=8):
    ss = sentences(text)
    if not ss:
        return "No readable text was found."
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]+", text.lower())
    freq = Counter(w for w in words if w not in STOP and len(w) > 2)
    scored = []
    for i, s in enumerate(ss):
        sw = re.findall(r"[A-Za-z][A-Za-z0-9'-]+", s.lower())
        score = sum(freq[w] for w in sw if w in freq) / max(1, len(sw))
        scored.append((score, i, s))
    chosen = sorted(scored, reverse=True)[:max_sentences]
    return " ".join(s for _, _, s in sorted(chosen, key=lambda x: x[1]))

def retrieve(question, text, k=4):
    chunks = chunk_text(text)
    if not chunks:
        return []
    vect = TfidfVectorizer(stop_words="english")
    mat = vect.fit_transform(chunks + [question])
    scores = cosine_similarity(mat[-1], mat[:-1]).ravel()
    idx = scores.argsort()[::-1][:k]
    return [chunks[i] for i in idx if scores[i] > 0]

def ollama_generate(prompt, model="qwen3:4b"):
    try:
        r = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=90
        )
        if r.ok:
            return r.json().get("response", "").strip()
    except Exception:
        pass
    return None

def answer_question(question, text):
    context = retrieve(question, text)
    if not context:
        return "I could not find relevant information in the uploaded material."
    prompt = f"""You are a study assistant. Answer only from the provided context.
If the context does not contain the answer, say that it is not available.
Question: {question}

Context:
{chr(10).join(context)}

Give a clear student-friendly answer with short bullets when useful."""
    generated = ollama_generate(prompt)
    if generated:
        return generated
    return "Local retrieval result:\n\n" + "\n\n".join(context)
