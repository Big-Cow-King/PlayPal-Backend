from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, \
    OutstandingToken
from rest_framework.permissions import IsAuthenticated
from registration.serializers import UserSerializer


class SignUpView(CreateAPIView):
    queryset = User.objects.all()  # Declare the set of objects to operate on
    serializer_class = UserSerializer


class LogOutView(APIView):
    """
    Reference: https://medium.com/django-rest/logout-django-rest-framework-eb1b53ac6d35
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_200_OK)


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
        username = request.POST.get('username', '')
        password = request.POST.get('password',
                                    '')  # 这个版本更加安全，如果没有password，default会用''
        email = request.POST.get('email', '')
        if User.objects.filter(username=username).exists():
            error = {"error": "Username already exists"}
            messages = f'FAILED: Account {username}creation failed - Username already exists'
            return send_response(409, messages, error)
        if User.objects.filter(email=email).exists():
            error = {"error": "email already exists"}
            messages = f'FAILED: email {email} creation failed - email already exists'
            return send_response(409, messages, error)
        if username != '' and password != '' and email != '':
            User.objects.create_user(username=username, password=password
                                     , email=email)
            messages = f'Account created for {username}!'
            return send_response(200, messages)
        else:
            error = {"error": [username, password, email]}
            messages = f'FAILED: Account creation failed!'
            return send_response(400, messages, error)
    else:
        messages = f'FAILED: method is not POST'
        return send_response(405, messages)
