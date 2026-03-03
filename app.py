from flask import Flask, request, render_template_string
import requests
import json
import re

app = Flask(__name__)

# Load knowledge base
with open("knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

def retrieve_context(question):
    question_lower = question.lower()
    matched = []

    for entry in knowledge_base:
        score = 0
        for word in question_lower.split():
            if word in entry["content"].lower():
                score += 1
        if score >= 2:
            matched.append(entry["content"])

    return "\n\n".join(matched)

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

HTML = """
<!doctype html>
<html>
<head>
    <title>Steve Jobs (1996) Persona</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f7;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
        }
        .chat-box {
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            background: #fafafa;
        }
        .user {
            text-align: right;
            margin: 10px 0;
        }
        .assistant {
            text-align: left;
            margin: 10px 0;
        }
        .bubble {
            display: inline-block;
            padding: 10px 14px;
            border-radius: 12px;
            max-width: 70%;
        }
        .user .bubble {
            background: #007aff;
            color: white;
        }
        .assistant .bubble {
            background: #e5e5ea;
            color: black;
        }
        form {
            display: flex;
            gap: 10px;
        }
        input[name="question"] {
            flex: 1;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }
        button {
            padding: 10px 16px;
            border-radius: 6px;
            border: none;
            background: black;
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Steve Jobs (1955–1996)</h2>

        <div class="chat-box">
            {% if question %}
            <div class="user">
                <div class="bubble">{{question}}</div>
            </div>
            {% endif %}

            {% if answer %}
            <div class="assistant">
                <div class="bubble">{{answer}}</div>
            </div>
            {% endif %}
        </div>

        <form method="post">
            <input name="question" placeholder="Ask Steve Jobs (1996)..." required>
            <button type="submit">Send</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None

    if request.method == "POST":
        question = request.form["question"]

        context = retrieve_context(question)

        prompt = f"""
You are Steve Jobs in December 1996.
You may ONLY use the information explicitly stated in the Context.
If the answer is not in the Context, say:
"I do not have information about that within my current timeline."

Context:
{context}

Question:
{question}

Answer:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "steve1996",
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        model_answer = response.json()["response"]

        if output_violates_timeline(model_answer):
            answer = "That falls outside my current timeline."
        else:
            answer = model_answer

    return render_template_string(HTML, answer=answer, question=request.form.get("question"))

if __name__ == "__main__":
    app.run(debug=True)