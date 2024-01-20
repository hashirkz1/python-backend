# ml_script.py
import joblib
import numpy as np
from scipy.io import wavfile

def load_model(model_path):
    return joblib.load(model_path)

def process_audio(model, audio_file_path):
    # Load the audio file
    sample_rate, audio_data = wavfile.read(audio_file_path)

    # Your audio processing logic goes here
    # For demonstration purposes, let's just compute the mean of the audio data
    audio_mean = np.mean(audio_data)

    # Use the loaded machine learning model to make predictions or further processing
    model_prediction = model.predict(audio_data.reshape(1, -1))  # Example: Predict using the entire audio_data

    return audio_mean, model_prediction[0]

if __name__ == "__main__":
    # Replace 'Best_Model (1).sav' with the actual path to your serialized machine learning model
    model_path = 'Best_Model (1).sav'
    
    # Replace 'path/to/your/audio/file.wav' with the actual path to your audio file
    audio_file_path = 'audio.wav'

    # Load the machine learning model
    ml_model = load_model(model_path)

    # Process the audio file using the loaded model
    mean_value, model_prediction = process_audio(ml_model, audio_file_path)

    # Print or use the results as needed
    print(f'Mean of audio data: {mean_value}')
    print(f'Model prediction: {model_prediction}')
