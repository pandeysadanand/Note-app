from rest_framework import serializers

from note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'color', 'description', 'user_id', 'is_archive']

        def create(self, validated_data):
            """
            Create and return a new User instance,given to validate data
            """
            return Note.objects.create_note(**validated_data)
