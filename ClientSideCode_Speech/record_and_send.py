import requests
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
import pyttsx3
from transformers import pipeline

# Backend API endpoints
API_FETCH_QUESTIONS = "http://127.0.0.1:8000/api/fetch-questions/"
API_SAVE_ANSWER = "http://127.0.0.1:8000/api/save-answer/"

# Initialize Whisper model
model = whisper.load_model("base")

# Initialize TTS engine
engine = pyttsx3.init()

# Initialize NLP pipeline for intent recognition
nlp_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define intent categories
response_classes = ["affirmative", "negative", "unclear"]

def speak(text):
    """
    Convert text to speech for blind users.
    """
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=5, samplerate=16000):
    """
    Record audio from the microphone and save it as a WAV file.
    """
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_wav.name, samplerate, audio_data)
    return temp_wav.name

def transcribe_audio(file_path):
    """
    Transcribe audio using Whisper model.
    """
    print("Transcribing...")
    result = model.transcribe(file_path)
    return result['text'].strip().lower()

def analyze_intent(user_response):
    """
    Analyze the user's intent dynamically using NLP.
    """
    result = nlp_pipeline(user_response, candidate_labels=response_classes)
    top_label = result['labels'][0]
    confidence = result['scores'][0]
    return top_label if confidence > 0.6 else "unclear"

def send_answer_to_backend(question_id, answer):
    """
    Send the user's answer to the backend API.
    """
    payload = {
        "question_id": question_id,
        "answer": answer
    }
    response = requests.post(API_SAVE_ANSWER, json=payload)
    return response.json()

def fetch_questions():
    """
    Fetch the list of questions from the backend API.
    """
    response = requests.get(API_FETCH_QUESTIONS)
    return response.json().get('questions', [])

def dynamic_interaction(question_id, question_text):
    """
    Handle dynamic interaction for each question.
    """
    while True:
        # Read the question and give the user thinking time
        speak(f"Question: {question_text}")
        speak("Take your time to think. When ready, speak your answer.")

        # Wait 10 seconds before prompting the user for input
        for i in range(10):
            speak(f"{10 - i} seconds remaining.")

        speak("Please speak your answer now.")
        audio_file = record_audio()
        transcription = transcribe_audio(audio_file)
        os.remove(audio_file)

        # Confirm the transcription with the user
        speak(f"I heard: {transcription}. Is this correct? Please say yes or no.")
        confirmation_audio = record_audio(duration=3)
        confirmation = transcribe_audio(confirmation_audio)
        os.remove(confirmation_audio)

        # Analyze intent to determine confirmation
        intent = analyze_intent(confirmation)
        if intent == "affirmative":
            response = send_answer_to_backend(question_id, transcription)
            if response.get("success"):
                speak("Your answer has been saved successfully.")
            else:
                speak("There was an error saving your answer. Please try again.")
            break
        elif intent == "negative":
            speak("Let's try again. Take your time to think.")
        else:
            speak("I didn't understand. Please repeat.")

def main():
    """
    Main function to guide the user through the exam process.
    """
    # Fetch the list of questions from the backend
    questions = fetch_questions()
    if not questions:
        speak("No questions are available right now. Please try again later.")
        return

    # Guide the user through each question
    for idx, question in enumerate(questions, start=1):
        speak(f"Question {idx} out of {len(questions)}.")
        dynamic_interaction(question['id'], question['question'])

    # End of exam interaction
    speak("You have completed the exam. Thank you for your responses.")

if __name__ == "__main__":
    main()
