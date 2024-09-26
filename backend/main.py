from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# NON TOCCARE QUESTA PARTE DI CODICE
app = Flask(__name__)

# Configurazione CORS
CORS(app)

# Percorso del file JSON
DB_FILE = 'db.json'

# Funzione per leggere i task dal file JSON
def load_tasks():
    if not os.path.exists(DB_FILE):
        # Se il file non esiste, inizializzalo
        with open(DB_FILE, 'w') as f:
            json.dump({"_default": []}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f).get("_default", [])

# Funzione per salvare i task nel file JSON
def save_tasks(task_list):
    with open(DB_FILE, 'w') as f:
        json.dump({"_default": task_list}, f)

# Endpoint per la creazione di un task
@app.route('/createTask', methods=['POST'])
def create_task():
    task_list = load_tasks()
    data = request.json
    
    # Validazione dei dati in arrivo
    if 'text' not in data or not data['text'].strip():
        return jsonify({"error": "Il campo 'text' è richiesto"}), 400

    nuovo_task = {
        'id': len(task_list) + 1,  # Incremento l'ID
        'text': data['text'],
        'isComplete': data.get('isComplete', False)  # Valore di default False
    }
    
    task_list.append(nuovo_task)
    save_tasks(task_list)
    
    return jsonify({"message": "Task creato con successo", "task": nuovo_task}), 201

# Endpoint per la visualizzazione dei task
@app.route('/getTasks', methods=['GET'])
def get_tasks():
    task_list = load_tasks()
    return jsonify(task_list), 200

# Endpoint per la cancellazione di un task
@app.route('/deleteTask/<int:id>', methods=['DELETE'])
def delete_task(id):
    task_list = load_tasks()
    task_list = [task for task in task_list if task['id'] != id]
    save_tasks(task_list)
    
    return jsonify({"message": f"Task con ID {id} cancellato con successo"}), 200

# NON TOCCARE QUESTA PARTE DI CODICE

# Esecuzione del server
if __name__ == '__main__':
    app.run(port='8080', debug=True)
