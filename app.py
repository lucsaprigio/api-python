from flask import Flask, request, jsonify
from models.task import Task

# __name__ = "__main__" if this file is run directly
app = Flask(__name__)

tasks  = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control # Pega a referencia da variável que está fora do método
    data = request.get_json()
    new_task = Task(id=task_id_control ,title=data['title'], description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({"message": "Nova tarefa criada por sucesso.", "id": new_task.id})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
        "tasks":task_list,
        "total_tasks":len(task_list),
    }

    return jsonify(output)
# F073

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())

    return jsonify({"message": "Tarefa não encontrada."}), 404


@app.route('/user/<user_id>')
# Criando variáveis como parâmetros da rota
def show_user(user_id):
    return f"User: {user_id}"

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
    
    if task == None:
        return jsonify({"message": "Tarefa não encontrada."}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    return jsonify({"message": "Tarefa atualizada com sucesso"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = id
    
    if not task:
        return jsonify({"message": "Tarefa não encontrada."}), 404

    task.remove(task)
    return jsonify({"message": "Tarefa removida com sucesso."})

if __name__ == "__main__":
    app.run(debug=True) # Debug habilitado para desenvolvimento
