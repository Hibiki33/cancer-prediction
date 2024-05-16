from django.shortcuts import render
import matplotlib
# matplotlib.use('WebAgg')

import gc
import torch
import numpy as np
import cv2
from torch.nn import functional as F
from os import listdir, makedirs, getcwd
import os
from os.path import join, exists, isfile, isdir, basename
from glob import glob
from ipywidgets import interact, widgets, FileUpload
from IPython.display import display
from matplotlib import patches as patches
from matplotlib import pyplot as plt
from copy import deepcopy
from segment_anything import sam_model_registry
from django.conf import settings
import shutil

# Setup Model
medsam_model = sam_model_registry['vit_b'](checkpoint=settings.MedSAM_CKPT_PATH)
medsam_model = medsam_model.to(settings.DEVICE)
medsam_model.eval()

@csrf_exempt
def start_medsam(request):
    if request.method == 'POST':
        preview_path = request.POST.get('preview')
        file_name = os.path.basename(preview_path)
        print('preview_path:', preview_path)
        copy_path = os.path.join(settings.MEDIA_ROOT, 'medsam', file_name)
        shutil.copyfile(preview_path, copy_path)