import logging

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer
from .utils import verify_token

logging.basicConfig(filename="view.log", filemode="w")


class NoteView(APIView):

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Add notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="color"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
                'is_archive': openapi.Schema(type=openapi.TYPE_STRING, description="is_archive")
            }
        ))
    @verify_token
    def post(self, request):
        """
            Registering note
        """
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Creates successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Update notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="color"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
                'is_archive': openapi.Schema(type=openapi.TYPE_STRING, description="is_archive")
            }
        ))
    @verify_token
    def put(self, request):
        """
            Updating existing note using id
        """
        note = Note.objects.get(pk=request.data.get('id'))
        serializer = NoteSerializer(note, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "data updated successfully", "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="delete note",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
            }
        ))
    @verify_token
    def delete(self, request):
        """
            Deleting particular note
        """
        try:
            note = Note.objects.get(pk=request.data['id'])
            note.delete()
            return Response({"message": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="get note by user_id")
    @verify_token
    def get(self, request):
        """
            Displaying note details
        """
        try:
            note = Note.objects.filter(user_id=request.data.get('user_id'))
            serializer = NoteSerializer(note, many=True)
            return Response({"message": "note found", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
