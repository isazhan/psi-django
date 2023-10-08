from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Main page'),
    path('create_project/', views.create_project, name='create_project'),
    path('<project_number>/', views.project, name='project'),
]