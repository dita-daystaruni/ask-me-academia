from django.db import models

class LectureNotes(models.Model):
    user_id = models.CharField(max_length=12)
    title = models.CharField(max_length=255)
    q_and_a = models.JSONField(blank=True, null=True)  # Field to store the Q&A dictionary
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
