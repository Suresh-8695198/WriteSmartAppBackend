# exam/serializers.py

from rest_framework import serializers

class SpeechInputSerializer(serializers.Serializer):
    audio_data = serializers.CharField(required=True)

class SaveAnswerSerializer(serializers.Serializer):
    question_id = serializers.CharField(required=True)
