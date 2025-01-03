from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import json
from difflib import get_close_matches

app = Flask(__name__)

DATA_FOLDER = "data"

# Cria o diretório de dados se ele não existir
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


def create_file(file_name: str):
    content = {"questions": [{"question": "Olá...", "answer": "Olá mundo..."}]}
    file_path = os.path.join(DATA_FOLDER, file_name)

    if not os.path.exists(file_path):
        with open(file_path, "w") as data:
            json.dump(content, data, indent=2)


def read_file_content(file_name: str):
    file_path = os.path.join(DATA_FOLDER, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        create_file(file_name)
        return {"questions": []}


def update_file_content(file_name: str, data: dict):
    file_path = os.path.join(DATA_FOLDER, file_name)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").lower()
        file_name = f"{username}.json"
        return redirect(url_for("chat", username=username))
    return render_template("index.html")


@app.route("/chat/<username>", methods=["GET", "POST"])
def chat(username):
    file_name = f"{username}.json"
    knowledge_base = read_file_content(file_name)

    if request.method == "POST":
        user_input = request.form.get("user_input")
        questions = [q["question"].lower() for q in knowledge_base["questions"]]
        best_match = find_best_match(user_input.lower(), questions)

        if best_match:
            for q in knowledge_base["questions"]:
                if q["question"].lower() == best_match:
                    return jsonify({"response": q["answer"]})
        else:
            new_answer = request.form.get("new_answer")
            if new_answer:
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                update_file_content(file_name, knowledge_base)
                return jsonify({"response": "Agora eu entendi! Obrigado por ensinar."})
            return jsonify({"response": "Não sei como responder. Pode me ensinar?"})

    return render_template("chat.html", username=username)


if __name__ == "__main__":
    app.run(debug=True)
