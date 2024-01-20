# audio_processing_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import os
import subprocess

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

                    
        # # Call your ML model here
        # # Replace the following line with your ML model code
        ml_script = 'backend/api/script.py'

        subprocess.run(['python',ml_script, audio_file])

        # # Assuming your model generates two output files
        output_file1 = 'audio_file_est1.wav'
        output_file2 = 'audio_file_est2.wav'
        print(output_file1 , output_file2)

        return Response({'filename': "output_file1"})
