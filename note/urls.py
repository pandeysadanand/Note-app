from django.urls import path

from note import views

urlpatterns = [
    path('note', views.NoteView.as_view(), name='note_api'),
]

