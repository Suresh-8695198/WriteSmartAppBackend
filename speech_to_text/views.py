from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("\\firebase\\firebase-admin-sdk.json")  # Replace with the correct path
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize OpenAI API
openai.api_key = "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"  # Replace with your OpenAI API key

@csrf_exempt
def fetch_questions(request):
    """
    Fetch questions from Firebase Firestore.
    """
    try:
        questions_ref = db.collection("exam_questions")
        questions = [{"id": doc.id, **doc.to_dict()} for doc in questions_ref.stream()]
        return JsonResponse({"questions": questions}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def speech_to_text(request):
    """
    Convert audio file to text using OpenAI Whisper API.
    """
    if request.method == "POST":
        try:
            audio_file = request.FILES.get("audio_file")
            if not audio_file:
                return JsonResponse({"error": "No audio file provided"}, status=400)

            temp_path = "temp_audio.wav"
            with open(temp_path, "wb") as f:
                f.write(audio_file.read())

            # Transcribe audio using Whisper API
            transcription = openai.Audio.transcribe("whisper-1", open(temp_path, "rb"))
            os.remove(temp_path)

            return JsonResponse({"transcription": transcription.get("text", "")}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def save_answer(request):
    """
    Save the answer to Firestore for the specified question ID.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question_id = data.get("question_id")
            answer = data.get("answer")

            if not question_id or not answer:
                return JsonResponse({"error": "Missing question_id or answer"}, status=400)

            db.collection("exam_questions").document(question_id).update({"answer": answer})

            return JsonResponse({"success": True, "message": "Answer saved successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
