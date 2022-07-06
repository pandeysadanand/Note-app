from rest_framework import serializers

from note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'color', 'description', 'user_id']
        # fields = '__all__'

        def update(self, instance, validated_data):
            instance.user_id = validated_data.get('user_id')
            instance.title = validated_data.get('title', instance.title)
            instance.color = validated_data.get('color', instance.color)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance

# one to one, fk,  many to many,object
# todo py test django(coverage report) requirement.txt file and create new venv