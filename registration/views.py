from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect
# yourappname/views.py
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse


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

    return JsonResponse(response_data,status=status)


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save the data in the database
            form.save()
            username = form.cleaned_data.get('username')
            messages = f'Account created for {username}!'
            send_response(200, messages)
        else:
            errors = form.errors
            messages = f'FAILED: Account created!'
            send_response(400, messages,errors)
    else:
        messages = f'FAILED: method is not POST'
        send_response(405, messages)
