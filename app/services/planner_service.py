from datetime import date

def make_plan(topic, exam_date, minutes_per_day):
    try:
        end = date.fromisoformat(exam_date)
        days = max(1, min(14, (end - date.today()).days))
    except Exception:
        days = 7
    lines = [f"AI Study Plan: {topic}", f"Daily study time: {minutes_per_day} minutes", ""]
    for i in range(1, days + 1):
        focus = ("Revision + self-test + weak-topic review" if i == days else
                 "Practice questions + active recall" if i % 3 == 0 else
                 "Core concepts + examples" if i % 2 == 0 else
                 "Read material + make concise notes")
        lines.append(f"Day {i}: {focus} ({minutes_per_day} min)")
    return "\n".join(lines)
