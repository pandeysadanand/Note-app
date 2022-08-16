from django.urls import path

from note import views

urlpatterns = [
    path('note', views.NoteView.as_view(), name='note_api'),
    path('collaborate', views.Collaborator.as_view(), name='collaborate_api'),
    path('label', views.LabelView.as_view(), name='label'),
    path('note_label', views.NoteLabel.as_view(), name='note_label_api'),
]
