import os
import random

DATA_PATH = "data/enron_sample.txt"


def load_dataset():
    if not os.path.exists(DATA_PATH):
        return generate_fallback()

    emails = []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f.readlines():
            text = line.strip()

            if not text:
                continue

            label = classify_label(text)

            emails.append({
                "text": text,
                "label": label
            })

    random.shuffle(emails)
    return emails


# ---------- SIMPLE HEURISTIC LABELING ----------

def classify_label(text):
    text = text.lower()

    # PRIORITY ORDER
    if any(k in text for k in ["asap", "urgent", "deadline", "immediately"]):
        return "urgent"

    if any(k in text for k in ["free", "win", "offer", "$", "prize"]):
        return "spam"

    return "important"


# ---------- FALLBACK DATA ----------

def generate_fallback():
    base = [
        "Win a free iPhone now!!!",
        "Meeting at 5pm",
        "Client escalation ASAP",
        "Lunch tomorrow?"
    ]

    data = []

    for _ in range(500):
        text = random.choice(base)
        data.append({
            "text": text,
            "label": classify_label(text)
        })

    return data