from rest_framework import serializers

from note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'color', 'description', 'user_id']

        # fields = '__all__'

        # def update(self, instance, validated_data):
        #     instance.user_id = validated_data.get('user_id')
        #     instance.title = validated_data.get('title', instance.title)
        #     instance.color = validated_data.get('color', instance.color)
        #     instance.description = validated_data.get('description', instance.description)
        #     instance.save()
        #     return instance

        def create(self, validate_data):
            notes = Note.objects.create(
                title=validate_data.get("title"),
                color=validate_data.get("color"),
                description=validate_data.get("description"),
                user_id=validate_data.get("user_id"),
            )
            return notes

# one to one, fk,  many to many,object
# todo py test django(coverage report) requirement.txt file and create new venv


