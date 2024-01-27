from django.urls import path

from .api.done import sign_up, user_login

urlpatterns = [
    path('sign_up/', sign_up, name='sign_up'),  # 定义一个名为 home 的 URL，并关联到 views 中的 home 函数
    path('login/', user_login, name='login'),
]
