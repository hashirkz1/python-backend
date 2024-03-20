from rest_framework.decorators import api_view
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

# audio_processing_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import os
import pandas as pd
import subprocess
import torch
from .models import AudioModel
import os

from torch import optim
from pytorch_lightning import Trainer
import soundfile as sf
from torch import optim
import pickle
import os
import base64

class AudioProcessingView(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request):
        audio_file = request.FILES.get('audiofile')
        print(request.FILES)

        if audio_file:
            media_directory = 'media'
            os.makedirs(media_directory, exist_ok=True)
            save_path = os.path.join(media_directory, audio_file.name)
            save_path = f'media/audio.wav'
            with open(save_path, 'wb') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

        file1,file2=runModel(save_path)
        
        with open(os.path.join(f'{file1}'), 'rb') as f:
            audio_data1 = f.read()
        with open(os.path.join(f'{file2}'), 'rb') as f:
            audio_data2 = f.read()
        
        # Encode audio files to base64
        audio_base64_1 = base64.b64encode(audio_data1).decode('utf-8')
        audio_base64_2 = base64.b64encode(audio_data2).decode('utf-8')
        
        # Return response
        return Response({"file1": audio_base64_1, "file2": audio_base64_2})
    
def runModel(path):
    # Passing the audio file path to the best_model.sav file to split the audio file into 2 files and then saving and returing the path of the file with the voice

    model = pd.read_pickle(os.path.join('Best_Model.sav'))
    model.separate(path, force_overwrite=True,resample=True)
    pathList=path.split("/")
    file,exe=pathList[-1].split(".")
    return "/".join(pathList[:-1])+"/"+file+"_est1."+exe,"/".join(pathList[:-1])+"/"+file+"_est2."+exe


@csrf_exempt
@api_view(['POST'])
def live_audio(request):
    try:
        file = request.FILES['file']
        audio_model = AudioModel.objects.create(audio_file=file)
        audio_model.save()
        image_path = audio_model.audio_file.url
        # This is the path we set in settings - MEDIA_URL = '/uploads/'
        new_path = "."+image_path
        print("New Path", image_path)
        audio_response = ''
        # runModel(new_path)
        path1, path2 = runModel(new_path)
        # print(image_label)

        success_response = {
            'result': 'success',
            'message': 'File uploaded successfully',
            'audio_label': audio_response,
        }
        response = JsonResponse(success_response)
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        file_response = FileResponse(file.open(), content_type='image/jpeg')  # Adjust content_type as needed
        response.streaming_content = file_response.streaming_content
        return response
    except Exception as e:
        print(e)
        error_response = {
            'result': 'error',
            'message': str(e),
        }
        return JsonResponse(error_response, status=500)