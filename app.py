from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import os
import json
from rapidfuzz import process, fuzz
import re
from unidecode import unidecode


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para sessions

DATA_FOLDER = "data"

# Cria a pasta de dados, se não existir
os.makedirs(DATA_FOLDER, exist_ok=True)


def normalize_text(text):
    """Normaliza o texto para melhor comparação"""
    text = unidecode(text.lower())  # Remove acentos e coloca em minúsculas
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    text = re.sub(r'\s+', ' ', text).strip()  # Remove espaços extras
    return text

# Função para criar um novo arquivo de conhecimento
def create_file(file_name: str):
    content = {
        "questions": [
            {"question": "Olá", "answer": "Olá! Como posso ajudar?"},
            {"question": "Qual é o seu nome?", "answer": "Eu sou um assistente virtual Etham!", "variations": ["como você se chama?", "qual seu nome?"]}
        ]
    }
    file_path = os.path.join(DATA_FOLDER, file_name)

    if not os.path.exists(file_path):
        with open(file_path, "w") as data:
            json.dump(content, data, indent=2)


# Função para ler conteúdo de um arquivo
def read_file_content(file_name: str):
    file_path = os.path.join(DATA_FOLDER, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        create_file(file_name)
        return {"questions": []}


# Função para atualizar conteúdo de um arquivo
def update_file_content(file_name: str, data: dict):
    file_path = os.path.join(DATA_FOLDER, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


# Função para encontrar a melhor correspondência
def find_best_match(user_question: str, knowledge_base: list):
    """Encontra a melhor correspondência considerando variações"""
    normalized_input = normalize_text(user_question)
    
    # Primeiro verifica correspondência exata
    for q in knowledge_base["questions"]:
        normalized_q = normalize_text(q["question"])
        if normalized_input == normalized_q:
            return q["answer"]
        
        # Verifica variações
        for variation in q.get("variations", []):
            if normalized_input == normalize_text(variation):
                return q["answer"]
    
    # Se não encontrou exato, usa fuzzy matching
    all_possibilities = []
    for q in knowledge_base["questions"]:
        all_possibilities.append((q["question"], q["answer"]))
        for variation in q.get("variations", []):
            all_possibilities.append((variation, q["answer"]))
    
    questions_list = [q[0] for q in all_possibilities]
    best_match = process.extractOne(
        user_question,
        questions_list,
        scorer=fuzz.token_sort_ratio,  # Melhor para ordem diferente de palavras
        score_cutoff=70
    )
    
    if best_match:
        index = questions_list.index(best_match[0])
        return all_possibilities[index][1]
    
    return None


# Rota do chat
@app.route("/", methods=["GET", "POST"])
def chat(username="etham"):

    #username = session.get('username', 'etham') 
    file_name = f"{username}.json"
    knowledge_base = read_file_content(file_name)

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        
        if not user_input:
            return jsonify({"response": "Por favor, digite algo."})
        
        response = find_best_match(user_input, knowledge_base)
        
        if response:
            return jsonify({"response": response})
        else:
            # Se não souber responder, armazena para aprendizado futuro
            learning_file = f"{username}_learning.json"
            learning_base = read_file_content(learning_file)
            learning_base["questions"].append({
                "question": user_input,
                "answer": "",
                "context": request.form.get("context", "")
            })
            update_file_content(learning_file, learning_base)
            
            return jsonify({
                "response": "Não sei responder isso ainda. Poderia me ensinar?",
                "needs_teaching": True,
                "original_question": user_input
            })

    return render_template("chat.html", username=username)
from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import os
import json
from rapidfuzz import process
import re
from unidecode import unidecode


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para sessions

DATA_FOLDER = "data"

# Cria a pasta de dados, se não existir
os.makedirs(DATA_FOLDER, exist_ok=True)


def normalize_text(text):
    """Normaliza o texto para melhor comparação"""
    text = unidecode(text.lower())  # Remove acentos e coloca em minúsculas
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    text = re.sub(r'\s+', ' ', text).strip()  # Remove espaços extras
    return text

# Função para criar um novo arquivo de conhecimento
def create_file(file_name: str):
    content = {
        "questions": [
            {"question": "Olá", "answer": "Olá! Como posso ajudar?"},
            {"question": "Qual é o seu nome?", "answer": "Eu sou um assistente virtual Etham!", "variations": ["como você se chama?", "qual seu nome?"]}
        ]
    }
    file_path = os.path.join(DATA_FOLDER, file_name)

    if not os.path.exists(file_path):
        with open(file_path, "w") as data:
            json.dump(content, data, indent=2)


# Função para ler conteúdo de um arquivo
def read_file_content(file_name: str):
    file_path = os.path.join(DATA_FOLDER, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        create_file(file_name)
        return {"questions": []}


# Função para atualizar conteúdo de um arquivo
def update_file_content(file_name: str, data: dict):
    file_path = os.path.join(DATA_FOLDER, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


# Função para encontrar a melhor correspondência
def find_best_match(user_question: str, knowledge_base: list):
    """Encontra a melhor correspondência considerando variações"""
    normalized_input = normalize_text(user_question)
    
    # Primeiro verifica correspondência exata
    for q in knowledge_base["questions"]:
        normalized_q = normalize_text(q["question"])
        if normalized_input == normalized_q:
            return q["answer"]
        
        # Verifica variações
        for variation in q.get("variations", []):
            if normalized_input == normalize_text(variation):
                return q["answer"]
    
    # Se não encontrou exato, usa fuzzy matching
    all_possibilities = []
    for q in knowledge_base["questions"]:
        all_possibilities.append((q["question"], q["answer"]))
        for variation in q.get("variations", []):
            all_possibilities.append((variation, q["answer"]))
    
    questions_list = [q[0] for q in all_possibilities]
    best_match = process.extractOne(
        user_question,
        questions_list,
        scorer=fuzz.token_sort_ratio,  # Melhor para ordem diferente de palavras
        score_cutoff=70
    )
    
    if best_match:
        index = questions_list.index(best_match[0])
        return all_possibilities[index][1]
    
    return None


# Rota do chat
@app.route("/", methods=["GET", "POST"])
def chat(username="etham"):

    #username = session.get('username', 'etham') 
    file_name = f"{username}.json"
    knowledge_base = read_file_content(file_name)

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        
        if not user_input:
            return jsonify({"response": "Por favor, digite algo."})
        
        response = find_best_match(user_input, knowledge_base)
        
        if response:
            return jsonify({"response": response})
        else:
            # Se não souber responder, armazena para aprendizado futuro
            learning_file = f"{username}_learning.json"
            learning_base = read_file_content(learning_file)
            learning_base["questions"].append({
                "question": user_input,
                "answer": "",
                "context": request.form.get("context", "")
            })
            update_file_content(learning_file, learning_base)
            
            return jsonify({
                "response": "Não sei responder isso ainda. Poderia me ensinar?",
                "needs_teaching": True,
                "original_question": user_input
            })

    return render_template("chat.html", username=username)


# Rota de erro personalizado
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)


# Rota de erro personalizado
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
