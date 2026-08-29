from flask import Flask, request, render_template_string

app = Flask(__name__)

questions = [
    {
        "question": "Python is a ______ language?",
        "options": ["Programming", "Markup", "Database", "Operating System"],
        "answer": "Programming",
        "level": "Easy"
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "def", "fun", "define"],
        "answer": "def",
        "level": "Easy"
    },
    {
        "question": "Which data structure follows FIFO?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "answer": "Queue",
        "level": "Medium"
    },
    {
        "question": "What is the output of 2 ** 3?",
        "options": ["5", "6", "8", "9"],
        "answer": "8",
        "level": "Medium"
    },
    {
        "question": "What is the time complexity of Binary Search?",
        "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
        "answer": "O(log n)",
        "level": "Hard"
    }
]

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Adaptive Quiz Master</title>

<style>
body {
    font-family: Arial;
    background: linear-gradient(135deg,#667eea,#764ba2);
    margin: 0;
    padding: 50px;
}

.box {
    background: white;
    max-width: 600px;
    margin: auto;
    padding: 35px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

h1 {
    text-align: center;
    color: #4f46e5;
}

.question {
    font-size: 22px;
    margin: 25px 0;
}

.option {
    display: block;
    padding: 12px;
    margin: 10px 0;
    background: #f1f5f9;
    border-radius: 8px;
}

button {
    width: 100%;
    padding: 14px;
    background: #4f46e5;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 17px;
    cursor: pointer;
}

button:hover {
    background: #3730a3;
}

.level {
    text-align: center;
    color: #dc2626;
    font-weight: bold;
}
</style>
</head>

<body>

<div class="box">

{% if page == "start" %}

<h1>🧠 Adaptive Quiz Master</h1>

<p style="text-align:center;">
Test your knowledge!
</p>

<form method="POST">

<input type="hidden" name="action" value="start">

<input type="text"
       name="name"
       placeholder="Enter your name"
       required
       style="width:95%;padding:12px;">

<br><br>

<button type="submit">Start Quiz</button>

</form>

{% elif page == "quiz" %}

<h1>🧠 Adaptive Quiz</h1>

<p>Student: <b>{{ name }}</b></p>

<p>Question {{ number }} / 5</p>

<p class="level">
Difficulty: {{ level }}
</p>

<div class="question">
{{ question["question"] }}
</div>

<form method="POST">

<input type="hidden" name="action" value="answer">
<input type="hidden" name="number" value="{{ number }}">
<input type="hidden" name="score" value="{{ score }}">
<input type="hidden" name="level" value="{{ level }}">
<input type="hidden" name="name" value="{{ name }}">

{% for option in question["options"] %}

<label class="option">
<input type="radio"
       name="answer"
       value="{{ option }}"
       required>

{{ option }}
</label>

{% endfor %}

<br>

<button type="submit">Next Question →</button>

</form>

{% elif page == "result" %}

<h1>🎉 Quiz Completed!</h1>

<h2>Student: {{ name }}</h2>

<h2>Your Score: {{ score }} / 50</h2>

{% if score >= 40 %}

<h2 style="color:green;">Excellent! 🌟</h2>

{% elif score >= 30 %}

<h2 style="color:orange;">Good Performance! 👍</h2>

{% else %}

<h2 style="color:red;">Keep Practicing! 💪</h2>

{% endif %}

<br>

<a href="/">
<button>Take Quiz Again</button>
</a>

{% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        action = request.form.get("action")

        # START QUIZ
        if action == "start":

            name = request.form.get("name")

            return render_template_string(
                HTML,
                page="quiz",
                name=name,
                number=1,
                score=0,
                level="Easy",
                question=questions[0]
            )

        # ANSWER QUESTION
        if action == "answer":

            number = int(request.form.get("number"))
            score = int(request.form.get("score"))
            name = request.form.get("name")
            answer = request.form.get("answer")

            current_question = questions[number - 1]

            # Check answer
            if answer == current_question["answer"]:
                score += 10

            # Next question
            next_number = number + 1

            # Quiz completed
            if next_number > 5:

                return render_template_string(
                    HTML,
                    page="result",
                    name=name,
                    score=score
                )

            next_question = questions[next_number - 1]

            return render_template_string(
                HTML,
                page="quiz",
                name=name,
                number=next_number,
                score=score,
                level=next_question["level"],
                question=next_question
            )

    return render_template_string(
        HTML,
        page="start"
    )


if __name__ == "__main__":
    app.run(debug=True)

