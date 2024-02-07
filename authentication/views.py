# Create your views here.
# myapp/views.py
# from django.contrib.auth import authenticate
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.tokens import RefreshToken,AccessToken


# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#
#         if user := authenticate(username=username, password=password):
#             refresh = RefreshToken.for_user(user)
#             access = AccessToken.for_user(user)
#             refresh_token = str(refresh)
#             access_token = str(access)
#             message = f"successfully get username={username} from database"
#             return send_response(200, message, token={"refresh" : refresh_token,"access" : access_token})
#         else:
#             message = f"username or password incorrect"
#             return send_response(404, message)
#
#
# def send_response(status, message, error=None, token=None):
#     response_data = {'status': status, 'message': message}
#
#     if error is not None:
#         response_data['error'] = error
#     if token is not None:
#         response_data['token'] = token
#
#     return JsonResponse(response_data, status=status)

# myapp/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
# from .serializers import LoginSerializer
#
# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=200)

