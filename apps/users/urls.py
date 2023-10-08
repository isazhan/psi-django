from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.profile, name='profile'),
    path('profile/vacation/', views.vacation, name='vacation'),
    path('profile/vacation/addvacation/', views.add_vacation, name='add_vacation'),
    path('profile/application/', views.application, name='application'),
    path('sign_applications/', views.sign_applications, name='sign_applications'),
    path('accept_applications/<int:applications_id>/', views.accept_applications, name='accept_applications'),
    path('reject_applications/', views.reject_applications, name='reject_applications'),
    path('all_applications/', views.all_applications, name='all_applications'),
    path('delete_application/<int:application_id>/', views.delete_application, name='delete_application'),
    path('download_application/<int:application_id>/', views.download_application, name='download_application'),
    #path('permission_manage', views.permission_manage, name='permission_manage'),
]