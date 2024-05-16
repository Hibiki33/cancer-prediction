from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from pathlib import Path
import os
import shutil
from PIL import Image as PImage
from openslide import OpenSlide


# Create your views here.
@csrf_exempt
def upload_chunk(request):
    if request.method == 'POST':
        file_hash = request.POST.get('fileHash')
        print('fileHash:', request.POST.get('fileHash'))
        chunk = request.FILES.get('chunk')
        chunk_hash = request.POST.get('chunkHash')  # 分片的hash值作为文件名
        # chunk_sequence = request.POST.get('chunkSequence')  # 分片的序号

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', file_hash)
        Path(upload_dir).mkdir(parents=True, exist_ok=True)

        chunk_path = os.path.join(upload_dir, f"{chunk_hash}")
        with open(chunk_path, 'wb+') as file:
            for chunk in chunk.chunks():
                file.write(chunk)

        return JsonResponse({'ok': True, 'msg': '分片上传成功'}, status=200)

    return JsonResponse({'ok': False, 'msg': '请求方法不正确'}, status=405)


@csrf_exempt
def merge_chunks(request):
    if request.method == 'POST':
        file_hash = request.POST.get('fileHash')
        file_name = request.POST.get('fileName')
        extension = file_name[file_name.rfind('.'):]  # 提取文件后缀

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', file_hash)
        target_file_path = os.path.join(settings.MEDIA_ROOT, 'completed', f"{file_hash}{extension}")
        Path(os.path.dirname(target_file_path)).mkdir(parents=True, exist_ok=True)

        chunk_files = sorted([f for f in os.listdir(upload_dir)], key=lambda x: int(x.split('-')[-1]))
        with open(target_file_path, 'wb') as destination:
            for chunk_file in chunk_files:
                chunk_path = os.path.join(upload_dir, chunk_file)
                with open(chunk_path, 'rb') as source:
                    shutil.copyfileobj(source, destination)
                os.remove(chunk_path)
        
        # 检查文件哈希值
        
        compressed_image_path = compress_image(target_file_path, file_hash)

        shutil.rmtree(upload_dir)  # 删除分片目录
        return JsonResponse({'ok': True, 'msg': '文件合并成功', 'preview': compressed_image_path, 'completed': target_file_path}, status=200)

    return JsonResponse({'ok': False, 'msg': '请求方法不正确'}, status=405)

@csrf_exempt
def compress_image(file_path, file_hash, size=(1024, 1024)):
    # 打开原始图像
    print("file_path:", file_path)
    slide = OpenSlide(file_path)
    level = 2
    slide_image = slide.read_region((0, 0), level, slide.level_dimensions[level])
    slide_image = slide_image.convert("RGB")
    x,y = slide_image.size
    k = min(x,y)
    x = x * size[0] // k
    y = y * size[1] // k
    slide_image = slide_image.crop((0,0,k,k))
    slide_image = slide_image.resize(size, PImage.Resampling.LANCZOS)
    
    # 保存压缩后的图像到BytesIO对象
    output_image_path = f'media/compressed/{file_hash}.png'
    slide_image.save(output_image_path)
    
    # 创建一个Django可用的文件对象
    return output_image_path
