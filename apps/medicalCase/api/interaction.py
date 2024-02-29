import json
from django.http import JsonResponse

from django.views.decorators.http import require_POST, require_GET
from django.core.files.storage import FileSystemStorage

schedule = '''第一周期：
化疗：使用药物组合A，每三周进行一次，连续进行四个周期。
手术：在第三周期后进行乳腺保留手术。
放疗规划：在手术后进行放疗。
第二周期：
放疗：进行为期六周的放疗，每日进行，每周五天。
第三周期：
化疗：使用药物组合B，每三周进行一次，连续进行四个周期。
靶向治疗：开始使用靶向药物，每日口服。
第四周期：
靶向治疗：继续使用靶向药物，每日口服，持续至治疗方案结束。
免疫疗法：开始免疫疗法，每月一次，连续进行六个月。
第五周期：
免疫疗法：继续免疫疗法，每月一次，连续进行六个月。
支持性疗法：根据患者需要提供支持性疗法，包括对症治疗、营养支持等。'''


@require_GET
def get_schedule(request):

    return JsonResponse({"schedule": schedule})

@require_POST
def upload_picture(request):
    if request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        return JsonResponse({'message': 'success'}, status=200)

    return JsonResponse({'message': 'success'}, status=501)

