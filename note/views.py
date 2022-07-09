import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer


class NoteView(APIView):

    def put(self, request, pk):
        try:
            note_data = json.loads(request.body)
            note = Note.objects.get(pk=pk)
            serializer = NoteSerializer(note, data=note_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "data updated successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # data = json.loads(request.body)
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Creates successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            note = Note.objects.get(id=pk)
            note.delete()
            return Response({"message": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except note.DoesNotExist:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        try:
            if pk is None:
                note = Note.objects.all()
                serializer = NoteSerializer(note, many=True)
                return Response({"data": serializer.data})
            note = Note.objects.get(id=pk)

            serializer = NoteSerializer(note)
            return Response({'data': serializer.data})

        except Exception as e:
            return Response({"message": str(e)})
