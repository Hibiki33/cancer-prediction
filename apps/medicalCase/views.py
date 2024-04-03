from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Image, FileChunk
from PIL import Pimage
from openslide import OpenSlide
import numpy as np
from django.core.files.base import ContentFile
from io import BytesIO

class UploadFileForm(forms.Form):
    file_name = forms.CharField(max_length=50)
    file_data = forms.FileField()

# class ImageForm(forms.Form):
#     class Meta:
#         model = Image
#         fields = ['file_name', 'file_data']

# Create your views here.
@csrf_exempt  # 如果您正在测试，可以临时禁用 CSRF 保护
def upload_pic(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 这里处理您的文件，例如保存文件
            saved_pic = handle_uploaded_file(request.POST['file_name'] ,request.FILES['file_data'])
            Image.objects.create(image=saved_pic, case_id=1)
            return JsonResponse({'message': 'image uploaded successfully'}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


def handle_uploaded_file(fn, f):
    with open('media/images/'+fn, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return 'media/images/'+fn


@csrf_exempt
def upload_chunk(request):
    if request.method == 'POST':
        file_chunk = request.FILES.get('chunk')
        chunk_hash = request.POST.get('chunkHash')
        file_hash = request.POST.get('fileHash')
        filename = request.POST.get('fileName')
        index = request.POST.get('index')
        size = file_chunk.size if file_chunk else 0

        if file_chunk and chunk_hash and file_hash and filename is not None:
            # 保存文件块到磁盘
            chunk_model = FileChunk(
                file_hash=file_hash,
                chunk_hash=chunk_hash,
                index=index,
                filename=filename,
                size=size,
                chunk=file_chunk
            )
            chunk_model.save()

            return JsonResponse({'message': 'Chunk uploaded successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Missing data'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=405)

@csrf_exempt
def combine_chunks(request):
    file_hash = request.GET.get('file_hash')
    chunks = FileChunk.objects.filter(file_hash=file_hash).order_by('index')
    file_path = f'media/{file_hash}.svg'

    with open(file_path, 'wb') as file:
        for chunk in chunks:
            with chunk.chunk.open('rb') as chunk_file:
                file.write(chunk_file.read())

    # 重组完成后，您可以删除原始的文件块记录或文件，以节省空间
    FileChunk.objects.filter(file_hash=file_hash).delete()

    compressed_path = compress_image(file_path, file_hash)

    return JsonResponse({'file_path': file_path, 'compressed_path': compressed_path}, status=200)

@csrf_exempt
def compress_image(file_path, file_hash, size=(1024, 1024)):
    # 打开原始图像
    slide = OpenSlide(file_path)
    level = 2
    slide_image = slide.read_region((0, 0), level, slide.level_dimensions[level])
    slide_image = slide_image.convert("RGB")
    x,y = slide_image.size
    k = min(x,y)
    x = x * size[0] // k
    y = y * size[1] // k
    slide_image = slide_image.crop((0,0,k,k))
    slide_image = slide_image.resize(size, Image.Resampling.LANCZOS)
    
    # 保存压缩后的图像到BytesIO对象
    output_image_path = f'media/compressed/{file_hash}.png'
    slide_image.save(output_image_path)
    
    # 创建一个Django可用的文件对象
    return output_image_path
