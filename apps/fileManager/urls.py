from django.urls import path
from .views import upload_chunk, merge_chunks

urlpatterns = [
    path('uploadc/', upload_chunk, name='upload_chunk'),
    path('merge/', merge_chunks, name='merge_chunks'),
]
