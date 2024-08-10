from rest_framework import serializers
from .models import LectureNotes

class LectureNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureNotes
        fields = ['user_id', 'title', 'q_and_a', 'uploaded_at',]
        read_only_fields = ['q_and_a', 'uploaded_at']
