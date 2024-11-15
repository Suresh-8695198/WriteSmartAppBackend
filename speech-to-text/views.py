# exam/views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view
from firebase_admin import firestore
from .nlp_service import analyze_text
from .speech_service import process_speech_to_text

db = firestore.client()

@api_view(['POST'])
def start_exam(request):
    return Response({"message": "The exam has started. You can begin."})

@api_view(['POST'])
def speech_input(request):
    data = request.data
    audio_data = data.get('audio_data')  # Assume this contains base64-encoded audio data
    
    # Convert speech to text
    text = process_speech_to_text(audio_data)
    request.session['current_answer'] = text  # Temporarily store in session
    return Response({"message": "Speech processed", "text": text})

@api_view(['POST'])
def preview_answer(request):
    text = request.session.get('current_answer', '')
    analyzed_text = analyze_text(text)  # Analyze using NLP
    return Response({
        "text": analyzed_text["text"],
        "stop_word_suggestions": analyzed_text["stop_word_suggestions"],
        "sentiment": analyzed_text["sentiment"],
        "grammar_suggestions": analyzed_text["grammar_suggestions"]
    })

@api_view(['POST'])
def save_answer(request):
    data = request.data
    question_id = data.get('question_id')
    text = request.session.get('current_answer', '')

    # Store answer in Firebase
    db.collection('exams').document('current_exam').collection('answers').document(question_id).set({
        'answer': text
    })
    return Response({"message": "Answer saved successfully."})

@api_view(['POST'])
def submit_all_answers(request):
    exam_ref = db.collection('exams').document('current_exam').collection('answers')
    all_answers = {doc.id: doc.to_dict() for doc in exam_ref.stream()}
    return Response({"message": "All answers submitted", "answers": all_answers})
