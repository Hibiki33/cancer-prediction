from django.urls import path
from .api.interaction import get_schedule, upload_picture
from .views import upload_pic, upload_chunk, combine_chunks

urlpatterns = [
    path('get_schedule', get_schedule, name='get_schedule'),
    # path('upload_picture/', upload_picture, name='upload_picture'),
    path('upload_pic', upload_pic, name='upload_pic'),
    path('combine_chunks/<str:file_hash>', combine_chunks, name='combine_chunks'),
    path('upload_chunk', upload_chunk, name='upload_chunk'), 
    path('get_compressed', )
]
