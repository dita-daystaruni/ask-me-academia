from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from AskMe.utility import get_questions_and_answers, process_pdf
from .models import LectureNotes
from .serializers import LectureNotesSerializer
from django.http import HttpResponse

class HomeView(APIView):
    def get(self, request):
        return HttpResponse("Welcome to Extraction API")

class LectureNotesUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = LectureNotesSerializer(data=request.data)
        multi_choice = True if request.data.get('multi_choice') == 'true' else False
        
        if file_serializer.is_valid():
            pdf_file = request.FILES.get('pdf_file')
            if not pdf_file:
                return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

            if not pdf_file.name.endswith('.pdf'):
                return Response({"error": "The uploaded file is not a PDF."}, status=status.HTTP_400_BAD_REQUEST)

            pdf_text = process_pdf(pdf_file)
            if pdf_text is None:
                return Response({"error": "The PDF does not contain extractable text or an error occurred."}, status=status.HTTP_400_BAD_REQUEST)

            questions_and_answers = get_questions_and_answers(pdf_text,multi_choice)
            if questions_and_answers is None:
                return Response({"error": "An error occurred while generating questions and answers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(questions_and_answers, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLectureNotesListView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        notes = LectureNotes.objects.filter(user_id=user_id)
        serializer = LectureNotesSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)