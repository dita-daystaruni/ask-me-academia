from django.urls import path
from .views import LectureNotesUploadView,UserLectureNotesListView

urlpatterns = [
    path('upload/', LectureNotesUploadView.as_view(), name='file-upload'),
    path('notes/<str:user_id>/', UserLectureNotesListView.as_view(), name='user_lecture_notes_list'),
]
