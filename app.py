from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import os
import json
from difflib import get_close_matches

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Altere para algo seguro em produção

DATA_FOLDER = "data"

# Cria a pasta de dados, se não existir
os.makedirs(DATA_FOLDER, exist_ok=True)


# Função para criar um novo arquivo de conhecimento
def create_file(file_name: str):
    content = {"questions": [{"question": "Olá", "answer": "Olá! Como posso ajudar?"}]}
    file_path = os.path.join(DATA_FOLDER, file_name)

    if not os.path.exists(file_path):
        with open(file_path, "w") as data:
            json.dump(content, data, indent=2)


# Função para ler conteúdo de um arquivo
def read_file_content(file_name: str):
    file_path = os.path.join(DATA_FOLDER, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        create_file(file_name)
        return {"questions": []}


# Função para atualizar conteúdo de um arquivo
def update_file_content(file_name: str, data: dict):
    file_path = os.path.join(DATA_FOLDER, file_name)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


# Função para encontrar a melhor correspondência
def find_best_match(user_question: str, questions: list):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Rota do chat
@app.route("/", methods=["GET", "POST"])
def chat(username="etham"):

    file_name = f"{username}.json"
    knowledge_base = read_file_content(file_name)

    if request.method == "POST":
        user_input = request.form.get("user_input").strip()
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
                return jsonify({"response": "Obrigado por me ensinar algo novo!"})
            return jsonify({"response": "Não sei como responder. Irei reencaminhar para o operador!"})

    return render_template("chat.html", username=username)


# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))


# Rota de erro personalizado
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
