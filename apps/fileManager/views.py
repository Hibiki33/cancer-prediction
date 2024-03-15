from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from pathlib import Path
import os
import shutil


# Create your views here.
@csrf_exempt
def upload_chunk(request):
    if request.method == 'POST':
        file_hash = request.POST.get('fileHash')
        chunk = request.FILES.get('chunk')
        chunk_name = request.POST.get('chunkHash')  # 分片的hash值作为文件名

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', file_hash)
        Path(upload_dir).mkdir(parents=True, exist_ok=True)

        chunk_path = os.path.join(upload_dir, chunk_name)
        with open(chunk_path, 'wb+') as file:
            for chunk in chunk.chunks():
                file.write(chunk)

        return JsonResponse({'ok': True, 'msg': '分片上传成功'})

    return JsonResponse({'ok': False, 'msg': '请求方法不正确'})


@csrf_exempt
def merge_chunks(request):
    if request.method == 'POST':
        file_hash = request.POST.get('fileHash')
        file_name = request.POST.get('fileName')
        extension = file_name[file_name.rfind('.'):]  # 提取文件后缀

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', file_hash)
        target_file_path = os.path.join(settings.MEDIA_ROOT, 'completed', f"{file_hash}{extension}")
        Path(os.path.dirname(target_file_path)).mkdir(parents=True, exist_ok=True)

        chunk_files = sorted([f for f in os.listdir(upload_dir)], key=lambda x: int(x.split('-')[1]))
        with open(target_file_path, 'wb') as destination:
            for chunk_file in chunk_files:
                chunk_path = os.path.join(upload_dir, chunk_file)
                with open(chunk_path, 'rb') as source:
                    shutil.copyfileobj(source, destination)
                os.remove(chunk_path)

        shutil.rmtree(upload_dir)  # 删除分片目录
        return JsonResponse({'ok': True, 'msg': '文件合并成功'})

    return JsonResponse({'ok': False, 'msg': '请求方法不正确'})
