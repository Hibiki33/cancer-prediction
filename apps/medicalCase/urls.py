from django.urls import path
from .api.interaction import get_schedule, upload_picture


urlpatterns = [
    path('get_schedule/', get_schedule, name='get_schedule'),
    path('upload_picture/', upload_picture, name='upload_picture'),
]
