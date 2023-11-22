from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_sqlalchemy import SQLAlchemy

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
api = Api(app)

app.config.update({
            'APISPEC_SPEC': APISpec(
                title='tasks crud',
                version='v1',
                openapi_version='2.0',
                plugins=[MarshmallowPlugin()],
            ),
            'APISPEC_SWAGGER_URL': '/swagger/',
        })
docs = FlaskApiSpec(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'complete': self.complete
        }


@app.route("/")
def index():
    todos = Todo.query.filter(Todo.complete == False)
    return render_template("index.html", todos=todos)

@app.route('/add', methods=["POST"])
def add():
    data = request.form["todo_item"]
    todo = Todo(text=data, complete=False)
    db.session.add(todo)
    db.session.commit()
    # return data # DEBUG REQUEST
    return redirect(url_for("index"))


@app.route('/update', methods=["POST"])
def update():
    ids = [int(i) for i in request.form.keys()]
        # Create a session
    with app.app_context():
        with db.session.begin():
            db.session.query(Todo).filter(Todo.id.in_(ids)).update({'complete': True}, synchronize_session='fetch')
        db.session.commit()
    return redirect(url_for("index"))

class TodoSchema(Schema):
    completed = fields.Bool(description="Признак активности", required=False, example=False)
    id = fields.Int(description="Номер записи", required=False, example=1)
    description = fields.Str(metadata={'description':"Название задачи", 'example':"eat good food"}, required = True)
    
class Tasks(MethodResource, Resource):
  

    @doc(description='get tasks list', tags=['Task'])
    @marshal_with(TodoSchema(many=True),code=200)
    def get(self):
        todos = Todo.query.filter(Todo.complete == False)
        task_list = [{'id': todo.id, 'description': todo.text, 'completed': todo.complete} for todo in todos]
        return task_list
    
    class PutTodoSchema(Schema):
        #description = fields.String(metadata={'description': 'Название задачи', 'example': 'eat good food'})
        description = fields.Str(metadata={"description":"Название задачи", "example":"test task"},required=True)
    
    class DeleteTodoSchema(Schema):
        id = fields.Int(metadata={'x-example': 1,'id': "id записи в бд"}, required=True)

    class Message(Schema):
        message = fields.String()

    @doc(description='add new task', tags=['Task'],consumes=['application/json'])
    @marshal_with(TodoSchema, code=200)
    @use_kwargs(PutTodoSchema)
    def put(self, description):
        todo = Todo(text=description, complete=False)
        try:
            db.session.add(todo)
            db.session.commit()
        except:
            return ({"message": "failed to save value to database"}, 500)
        return ({'id': todo.id, 'description': todo.text, 'completed': todo.complete}, 200)

    @doc(description='complete task.', tags=['Task'])
    @marshal_with(Message, code=200)
    @use_kwargs(DeleteTodoSchema, location='query')    
    def delete(self,id):
        #ids = [int(i.get('id')) for i in json_data]
        num =  id
        db.session.query(Todo).filter(Todo.id==num).delete()
        db.session.commit()
        return {'message':'data updated'}


api.add_resource(Tasks, '/api/task')
docs.register(Tasks)

if __name__ == '__main__':
    app.run(debug=True)