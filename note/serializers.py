from rest_framework import serializers

from note.models import Note, Label


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'color', 'description', 'user_id', 'is_archive']

        def create(self, validated_data):
            """
            Create and return a new User instance,given to validate data
            """
            return Note.objects.create(**validated_data)


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'title', 'color', 'user_id', "note"]
        read_only_fields = ["id", "color", "note"]
        # fields = "__all__"

        def create(self, validated_data):
            """
            Create and return a new label instance,given to validate data
            """
            return Label.objects.create(**validated_data)
