from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
from django.template import loader
from db import get_db_handle as db
from apps.main.decorators import permission_required

@login_required
def index(request):
    projects = Projects.objects.all()

    context = {
        'projects': projects,
    }
    
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context, request))


@permission_required('create_project')
def create_project(request):
    if request.method == 'POST': 
        col = db()['projects']
        data = {
            'project_number': request.POST['project_number'],
            'project_name': request.POST['project_name'],
        }
        x = col.insert_one(data)
        return index(request)
    else:
        return render(request, 'main/create_project.html')