from django.shortcuts import render, redirect
from db import get_db_handle as db

def permission_required(view_name):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            col = db()['permissions']
            query = { 'view_name':view_name, 'permission': request.user.username }
            if col.find_one(query):
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/')
        return wrap
    return decorator