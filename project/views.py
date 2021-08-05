from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .models import Project
import json

def json_decode(request):
    json_data = json.loads(request.body.decode("utf-8"))
    return json_data

def serialize(project):
    return serializers.serialize('json', [project, ])[1:-1]

def validate(project):
    pass

def save(data, user):
    name = data['name']
    bpm = data['bpm']
    lanes = data['lanes']
    project = Project(name=name, bpm=bpm, user=user, lanes=lanes)
    if not Project.objects.filter(user=user, name=name).exists():
        project.save()
    return project
    

def update():
    pass

def retrieve(user, project_name):
    project = Project.objects.get(user=user, name=project_name)
    response = serialize(project)
    return response

def retrieve_all(user):
    return Project.objects.filter(user=user)

def delete():
    pass

def delete_all(user):
    Project.objects.filter(user=user).delete()

def projects(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'GET':
            return render(request, 'index.html', {'projects':retrieve_all(user)})
        elif request.method == 'POST':
            project = json_decode(request)
            saved = serialize(save(project, user))
            return JsonResponse(saved, encoder=DjangoJSONEncoder, safe=False)
        elif request.method == 'DELETE':
            delete_all(user)
    else:
        return redirect('accounts/login/')

def project(request, id=id):
    if request.method == 'GET':
        return JsonResponse(retrieve(project), encoder=DjangoJSONEncoder, safe=False)
    elif request.method == 'PUT':
        project = json_decode(request)
        update()
    elif request.method == 'DELETE':
        delete(project, user)
        return HttpResponse('DELETED')
    return HttpResponse('OK')
