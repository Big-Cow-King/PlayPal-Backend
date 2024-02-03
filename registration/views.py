from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect
# yourappname/views.py
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def send_response(status, message, error=None):
    """
    Helper function to send JSON responses.

    Parameters:
    - status: str, status of the response ('success' or 'error').
    - message: str, a message providing details about the response.
    - data: dict, optional data to include in the response.

    Returns:
    - JsonResponse
    """
    response_data = {'status': status, 'message': message}

    if error is not None:
        response_data['error'] = error

    return JsonResponse(response_data, status=status)


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('Username', '')
        password = request.POST.get('Password',
                                    '')  # 这个版本更加安全，如果没有password，default会用''
        if username != '' and password != '':
            User.objects.create_user(username=username, password=password)
            messages = f'Account created for {username}!'
            return send_response(200, messages)
        else:
            error = {"error": [username, password]}
            messages = f'FAILED: Account created!'
            return send_response(400, messages, error)
    else:
        messages = f'FAILED: method is not POST'
        return send_response(405, messages)
