from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import tasks

def make_public_task(task):
    new_task = {}
    for field in task :
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'],
            _external = True )
        else :
            new_task[field] = task[field]
    return new_task
    
@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify(tasks =[make_public_task(t) for t in tasks])  #return un objet de type Response

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            return make_public_task(t)
    return 'Task not found'


@app.route('/todo/api/v1 .0/tasks', methods = ['POST'])
def create_task() :
    if not request.json or not 'title' in request.json :
        abort(400)
        task = {
            'id': tasks[-1]['id'] + 1 ,
            'title': request.json['title'],
            'description': request.json.get('description', " " ),
            'done': False
        }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201