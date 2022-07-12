import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer
from .utils import verify_token

logging.basicConfig(filename="view.log", filemode="w")


class NoteView(APIView):
    """
        Creating note view and performing crud operation
    """

    @verify_token
    def put(self, request):
        """
            Updating existing note using id
        """
        try:
            # note_data = json.loads(request.data)

            note = Note.objects.get(pk=request.data.get('note_id'))
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "data updated successfully", "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def post(self, request):
        """
            Registering note
        """
        serializer = NoteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Creates successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            # logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
            Deleting particular note
        """
        try:
            note = Note.objects.get(id=request.data.get('note_id'))
            note.delete()
            return Response({"message": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except note.DoesNotExist as dne:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
            Displaying note details
        """
        try:
            note = Note.objects.filter(user_id=request.data.get('user_id'))
            serializer = NoteSerializer(note, many=True)
            return Response({"message": "note found", "data": serializer.data}, status=status.HTTP_200_OK)
        except note.DoesNotExist as dne:
            return Response({"message": "note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
