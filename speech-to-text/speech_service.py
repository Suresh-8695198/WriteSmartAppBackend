# exam/speech_service.py

import io
from google.cloud import speech


def process_speech_to_text(audio_data):
    try:
        client = speech.SpeechClient()

        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US"
        )

        response = client.recognize(config=config, audio=audio)
        return response.results[0].alternatives[0].transcript
    except Exception as e:
        print("Error processing speech:", e)
        return ""
