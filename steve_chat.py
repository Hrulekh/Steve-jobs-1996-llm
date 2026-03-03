import requests
import json

# Load knowledge base
with open("knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

forbidden_keywords = [
    "iphone", "ipad", "ipod", "app store",
    "2000", "2001", "2007", "2010",
    "tim cook"
]

def is_forbidden(question):
    question_lower = question.lower()
    for word in forbidden_keywords:
        if word in question_lower:
            return True
    return False

def retrieve_context(question):
    question_lower = question.lower()
    matched = []

    for entry in knowledge_base:
        # Score how many words overlap
        score = 0

        for word in question_lower.split():
            if word in entry["content"].lower():
                score += 1

        if score >= 2:  # threshold
            matched.append(entry["content"])

    return "\n\n".join(matched)

import re

def output_violates_timeline(text):
    text_lower = text.lower()

    forbidden_terms = [
        "iphone", "ipad", "ipod", "tim cook",
        "2011", "2000", "2001", "2007", "2010",
        "pancreatic", "died", "death"
    ]

    for term in forbidden_terms:
        if term in text_lower:
            return True

    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    for year in years:
        if int(year) > 1996:
            return True

    return False


while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    if is_forbidden(user_input):
        print("\nSteve (1996): That falls outside my current timeline.")
        continue

    context = retrieve_context(user_input)

    prompt = f"""
You are Steve Jobs in December 1996.

You may ONLY use the information explicitly stated in the Context section.
Do NOT add new details.
Do NOT generalize beyond the context.
Do NOT soften historical conflicts.

If the Context does not contain the answer, respond exactly with:
"I do not have information about that within my current timeline."

Context:
{context}

Question:
{user_input}

Answer in first person:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "steve1996",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            print("API Error:", response.status_code)
            print(response.text)
            continue

        data = response.json()

        if "response" not in data:
            print("Unexpected API response:", data)
            continue

        answer = data["response"]
        if output_violates_timeline(answer):
            print("\nSteve (1996): That falls outside my current timeline.")
        else:
            print("\nSteve (1996):", answer.strip())

    except Exception as e:
        print("Error occurred:", e)