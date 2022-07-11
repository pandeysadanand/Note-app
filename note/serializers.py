from rest_framework import serializers

from note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'color', 'description', 'user_id']

        def create(self, validate_data):
            notes = Note.objects.create(
                title=validate_data.get("title"),
                color=validate_data.get("color"),
                description=validate_data.get("description"),
                user_id=validate_data.get("user_id"),
            )
            return notes

