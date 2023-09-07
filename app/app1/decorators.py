from .models import Uloga
from django.shortcuts import redirect

def profesor_required(function):
    def wrap(*args, **kwargs):
        if str(args[0].user.uloga) == 'PROFESOR':
            return function(*args, **kwargs)
        else:
            return redirect('home')
    return wrap 