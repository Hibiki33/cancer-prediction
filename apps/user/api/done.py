from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings

import json
from apps.user.models import User


@csrf_exempt
@require_POST
def sign_up(request):
    request_data = json.loads(request.body.decode('utf-8'))
    username = request_data.get('username')
    password = request_data.get('password')
    if username is None or password is None:
        return JsonResponse({"error": "Missing fields."}, status=401)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists."}, status=401)
    if password == '':
        return JsonResponse({"error": "Password cannot be empty."}, status=401)
    user = User.objects.create_user(username=username, password=password)

    return JsonResponse({"message": "User registered successfully."})


def user_login(request):
    obj = json.loads(request.body)
    username = obj.get('username', None)
    password = obj.get('password', None)
    if username is None or password is None:
        return JsonResponse({'code': 500, 'message': '请求参数错误'})

    is_login = authenticate(request, username=username, password=password)
    if is_login is None:
        return JsonResponse({'code': 500, 'message': '账号或密码错误'})

    login(request, is_login)

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(is_login)
    token = jwt_encode_handler(payload)
    return JsonResponse({'code': 200, 'message': '登录成功', 'data': {'token': token}})
