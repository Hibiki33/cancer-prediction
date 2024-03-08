from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Image

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
    