import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer
from .utils import verify_token

cursor = connection.cursor()

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
            cursor.execute(
                "insert into note_note (title,color,description,is_archive,user_id_id) values(%s,%s,%s,%s,%s)",
                [request.data['title'], request.data['color'], request.data['description'], request.data['is_archive'],
                 request.data['user_id']])
            return Response({"message": "Creates successfully"},
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

        try:
            cursor.execute("update note_note set title=%s,color=%s,description=%s,is_archive=%s where id=%s",
                           [request.data.get('title'),
                            request.data.get('color'),
                            request.data.get('description'),
                            request.data.get('is_archive'),
                            request.data.get('id')])
            return Response({"message": "data updated successfully"},
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
            pk = request.data['id']
            cursor.execute('delete from note_note where id=%s', [pk])
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
            note = Note.objects.raw(f"select * from note_note where user_id_id={request.data['user_id']}")
            serializer = NoteSerializer(note, many=True)
            return Response({"message": "note found", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
