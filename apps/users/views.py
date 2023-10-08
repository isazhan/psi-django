from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from pip._internal.commands import download
#from .models import *
from docxtpl import DocxTemplate
from django.conf import settings
#from .models import UserBackend
from django.contrib.auth.backends import BaseBackend


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username'] + '@psi-group.kz'
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print('login')
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'users/login.html', {'title': 'Страница входа'})
    else:
        return render(request, 'users/login.html', {'title': 'Страница входа'})


def logout_user(request):
    logout(request)
    return render(request, 'users/login.html', {'title': 'Страница входа'})


@login_required
def profile(request):
    users = CustomUser.objects.get(username=request.user)
    context = {
        'firstname': users.first_name,
        'lastname': users.last_name,
        'email': users.email,
    }
    template = loader.get_template('users/profile.html')
    return HttpResponse(template.render(context, request))


@login_required
def vacation(request):
    return render(request, 'users/vacation.html')


@login_required
def add_vacation(request):
    if request.method == "POST":
        startdate = request.POST['startdate']
        finishdate = request.POST['finishdate']
        duration = request.POST['duration']
        if request.POST['is_by_schedule'] == "on":
            is_by_schedule = True
        data = Vacations(username=request.user, startdate=startdate, finishdate=finishdate, duration=duration, is_by_schedule=is_by_schedule, supervisor='На рассмотрении')
        data.save()
        return render(request, 'users/vacation.html')
    else:
        return render(request, 'users/vacation.html')


@login_required
def application(request):
    applications = Vacations.objects.filter(username=request.user.id).values()
    return render(request, 'users/application.html', {'applications': applications})


@login_required
def sign_applications(request):
    # for supervisor
    vac_for_supervisor = Vacations.objects.select_related('username').filter(username__supervisor=request.user, supervisor = 'На рассмотрении')

    # for jun hr
    if request.user.position == 'jun_hr':
        vac_for_jun_hr = Vacations.objects.filter(jun_hr = 'На рассмотрении')
    else:
        vac_for_jun_hr = Vacations.objects.none()

    # for head hr
    if request.user.position == 'head_hr':
        vac_for_head_hr = Vacations.objects.filter(head_hr = 'На рассмотрении')
    else:
        vac_for_head_hr = Vacations.objects.none()

    # for director
    if request.user.position == 'director':
        vac_for_director = Vacations.objects.filter(director = 'На рассмотрении')
    else:
        vac_for_director = Vacations.objects.none()

    vacations = vac_for_supervisor | vac_for_jun_hr | vac_for_head_hr | vac_for_director

    context = {
        'vacations': vacations
    }
    template = loader.get_template('users/sign_applications.html')
    return HttpResponse(template.render(context, request))


@login_required
def accept_applications(request, applications_id):
    # sign as supervisor
    if Vacations.objects.select_related('username').get(id=applications_id).username.supervisor == str(request.user):
        x = Vacations.objects.get(id=applications_id)
        x.supervisor = 'Утверждено'
        x.jun_hr = 'На рассмотрении'
        x.save()

    # sign as jun hr
    if request.user.position == 'jun_hr':
        x = Vacations.objects.get(id=applications_id)
        x.jun_hr = 'Утверждено'
        x.head_hr = 'На рассмотрении'
        x.save()
    
    # sign as head hr
    if request.user.position == 'head_hr':
        x = Vacations.objects.get(id=applications_id)
        x.head_hr = 'Утверждено'
        x.director = 'На рассмотрении'
        x.save()
    
    # sign as director
    if request.user.position == 'director':
        x = Vacations.objects.get(id=applications_id)
        x.director = 'Утверждено'
        x.save()

    return redirect(sign_applications)


@login_required
def reject_applications(request):
    # reject as supervisor
    if Vacations.objects.select_related('username').get(id=request.POST['app-id']).username.supervisor == str(request.user):
        x = Vacations.objects.get(id=request.POST['app-id'])
        x.supervisor = 'Отклонено'
        x.comments = request.POST['comment']
        x.save()

    # reject as jun hr
    if request.user.position == 'jun_hr':
        x = Vacations.objects.get(id=request.POST['app-id'])
        x.jun_hr = 'Отклонено'
        x.comments = request.POST['comment']
        x.save()
    
    # reject as head hr
    if request.user.position == 'head_hr':
        x = Vacations.objects.get(id=request.POST['app-id'])
        x.head_hr = 'Отклонено'
        x.comments = request.POST['comment']
        x.save()
    
    # reject as director
    if request.user.position == 'director':
        x = Vacations.objects.get(id=request.POST['app-id'])
        x.director = 'Отклонено'
        x.comments = request.POST['comment']
        x.save()

    return redirect(sign_applications)

@login_required
def all_applications(request):
    if request.user.position == 'jun_hr' or request.user.position == 'head_hr':
        all_applications = Vacations.objects.all()
    else:
        all_applications = None
    return render(request, 'users/all_applications.html', {'all_applications': all_applications})

@login_required
def delete_application(request, application_id):
    if Vacations.objects.get(id=application_id).username == request.user:
        if Vacations.objects.get(id=application_id).supervisor == "На рассмотрении":
            Vacations.objects.get(id=application_id).delete()
    return redirect(application)

@login_required
def download_application(request, application_id):
    doc = DocxTemplate(settings.BASE_DIR / 'static/users/download_application.docx')
    if Vacations.objects.get(id=application_id).is_by_schedule == True:
        schedule = 'по графику'
    else:
        schedule = 'вне графика'

    context = {
        'surname': Vacations.objects.get(id=application_id).username,
        'startdate': Vacations.objects.get(id=application_id).startdate,
        'finishdate': Vacations.objects.get(id=application_id).finishdate,
        'duration': Vacations.objects.get(id=application_id).duration,
        'schedule' : schedule,
    }
    filename = Vacations.objects.get(id=application_id).username
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename={}.docx'.format(filename)
    doc.render(context)
    doc.save(response)

    return response


   # doc.render(context)
   # doc.save('application_output.docx')

   # return redirect(all_applications)
"""
from db import get_db_handle as db
def permission_manage(request):
    if 'permissions' not in db().list_collection_names():
        print('yes')
        col = db()['permissions']
    #context = {
    #    'projects': projects,
    #}

    template = loader.get_template('main/index.html')

    return HttpResponse(template.render(context, request))
"""