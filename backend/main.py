from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# NON TOCCARE QUESTA PARTE DI CODICE
app = Flask(__name__)

# Configurazione CORS
CORS(app)

# Percorso del file JSON
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.json')

# Funzione per leggere i task dal file JSON
def load_tasks():
    try:
        if not os.path.exists(DB_FILE):
            print(f"File {DB_FILE} non esiste. Creazione del file...")
            with open(DB_FILE, 'w') as f:
                json.dump({"_default": []}, f)
        with open(DB_FILE, 'r') as f:
            print(f"Caricamento del file {DB_FILE}")
            return json.load(f).get("_default", [])
    except Exception as e:
        print(f"Errore durante il caricamento dei task: {e}")
        return []

# Funzione per salvare i task nel file JSON
def save_tasks(task_list):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump({"_default": task_list}, f)
        print(f"Tasks salvati con successo su {DB_FILE}")
    except Exception as e:
        print(f"Errore durante il salvataggio dei task: {e}")

# Endpoint per la creazione di un task
@app.route('/createTask', methods=['POST'])
def create_task():
    task_list = load_tasks()
    data = request.json  
    print(f"Ricevuto JSON per creazione task: {data}") 

    # Validazione dei dati in arrivo
    if 'text' not in data or not data['text'].strip():
        return jsonify({"error": "Il campo 'text' è richiesto"}), 400

    nuovo_task = {
        'id': len(task_list) + 1, 
        'text': data['text'],
        'isComplete': data.get('isComplete', False)
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

# Endpoint per aggiornare un task (toggle completato/non completato)
@app.route('/updateTask/<int:id>', methods=['PUT'])
def update_task(id):
    task_list = load_tasks()
    data = request.json  
    print(f"Ricevuto JSON per aggiornamento task ID {id}: {data}") 
    
    # Trovare il task da aggiornare
    for task in task_list:
        if task['id'] == id:
            task['text'] = data.get('text', task['text'])  
            task['isComplete'] = data.get('isComplete', task['isComplete'])  
            break
    else:
        return jsonify({"error": "Task non trovato"}), 404

    save_tasks(task_list)
    return jsonify({"message": f"Task con ID {id} aggiornato con successo", "task": task}), 200

# NON TOCCARE QUESTA PARTE DI CODICE

# Esecuzione del server
if __name__ == '__main__':
    app.run(port='8080', debug=True)
