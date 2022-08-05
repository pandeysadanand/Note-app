from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from note import views

urlpatterns = [
    path('note', views.NoteView.as_view(), name='note_api'),
    path('note/<int:pk>', views.NoteDetails.as_view(), name='note_api'),
]

