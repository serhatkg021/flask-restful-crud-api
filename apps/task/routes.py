from flask import Flask, request

from .. import db, api
from .models import Task
from .resources import resource_fields
from flask_restful import Resource, reqparse, abort, marshal_with


def abort_if_task_doesnt_exist(pk):
    if pk not in Task.query.all():
        abort(404, message=f"Could not find task with that {pk}")


class TaskList(Resource):
    """
    Shows a list of all tasks, and lets you POST to add new tasks
    """
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        tasks = Task.query.order_by(Task.timestamp.desc()).all()
        return tasks, 201

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        data = request.json
        task = Task(name=data['name'], description=data['description'])
        db.session.add(task)
        db.session.commit()
        tasks = Task.query.order_by(Task.timestamp.desc()).all()
        return tasks, 201


class TaskSingle(Resource):
    """
    Shows a single todo item and lets you delete a todo item
    """
    @marshal_with(resource_fields, envelope='resource')
    def get(self, pk):
        abort_if_task_doesnt_exist(pk)
        task = Task.query.filter_by(id=pk).first()
        return task, 201

    @marshal_with(resource_fields, envelope='resource')
    def put(self, pk):
        abort_if_task_doesnt_exist(pk)
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        task.name = data['name']
        task.description = data['description']
        db.session.commit()
        return task, 201

    @marshal_with(resource_fields, envelope='resource')
    def delete(self, pk):
        abort_if_task_doesnt_exist(pk)
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.order_by(Task.timestamp.desc()).all()
        return tasks, 204


api.add_resource(TaskList, '/')
api.add_resource(TaskSingle, '/<int:pk>/')
