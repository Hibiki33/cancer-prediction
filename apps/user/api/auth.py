from datetime import timedelta

import jwt
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET


@response_wrapper
@require_GET
def refresh_token(request):
    """
    刷新token
    """
    try:
        # 从请求头中获取token
        header = request.META.get('HTTP_AUTHORIZATION')
        if header is None:
            raise jwt.InvalidTokenError
        # 解码token
        auth_info = header.split(' ')
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info
        if auth_type != 'Bearer':
            raise jwt.InvalidTokenError
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            print('InvalidTokenError')
            raise jwt.InvalidTokenError

        if payload['type'] != 'refresh_token':
            raise jwt.InvalidTokenError

        user_id = payload['user_id']
        record_id = payload['record_id']
        user = User.objects.filter(id=user_id).first()
        record = AuthRecord.objects.filter(id=record_id).first()

        if record is None or record.user != user:
            raise jwt.InvalidTokenError

        if record.expires_by < timezone.now():
            raise jwt.InvalidTokenError

        # 生成新的token
        token = generate_token(user)

        return success_api_response({'token': token})
    except jwt.InvalidTokenError:
        return failed_api_response(ErrorCode.INVALID_TOKEN_ERROR, '登录过期, token无效')


def byte2str(b):
    if type(b) is str:
        return b
    return b.decode('utf-8')