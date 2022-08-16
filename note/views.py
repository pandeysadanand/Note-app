import logging

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import Note, Label
from .serializers import NoteSerializer, LabelSerializer
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
        serializer = NoteSerializer(data=request.data)
        try:
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

        try:
            note = Note.objects.get(pk=request.data['id'])
            serializer = NoteSerializer(note, data=request.data)
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
            note = Note.objects.filter(user_id=request.data['user_id'])
            serializer = NoteSerializer(note, many=True)
            # user = User.objects.get(id=request.data['user_id'])
            # note = user.collaborator.all() | Note.objects.filter(user_id=request.data['user_id'])
            
            return Response({"message": "note found", "data": serializer.data},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LabelView(APIView):
    """label to the notes"""

    @verify_token
    def post(self, request):
        """
            # Creating a label
            param request: user_id, title, color, note_id
            return: response
        """
        serializer = LabelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # note_id_list = request.data.pop('note')
            #
            # label_list = Label.objects.filter(title=request.data.get('title'))
            #
            # label = label_list.first() if label_list.exists() else Label.objects.create(**request.data) # terninary operator
            # label.note.set(note_id_list)
            return Response({"message": "label created successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_200_OK)

    @verify_token
    def get(self, request):
        try:
            label = Label.objects.filter(user_id_id=request.data['user_id'])
            serializer = LabelSerializer(label, many=True)
            # print(request_data)
            # request_data = request.data
            # label_name = request_data.get("title")
            # label_data = Label.objects.get(title=label_name)
            # print(label_data)
            # note_data = label_data.Note.all()
            # note = Note.objects.filter(user_id=request_data["user_id"])
            # serializer = LabelSerializer(label, many=True)
            # print(note.note.all())
            return Response({
                "message": 'label found',
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        try:
            label = Label.objects.get(id=request.data.get("id"))
            label.delete()
            return Response({
                "message": "label delete successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(e)
            return Response({
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def put(self, request):
        """
            Updating existing note using id
        """

        try:
            label = Label.objects.get(pk=request.data['id'])
            serializer = LabelSerializer(label, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "data updated successfully", "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response({"message": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NoteLabel(APIView):
    @verify_token
    def post(self, request):
        try:
            print(request.data)
            label = Label.objects.get(title=request.data.get('title'))
            print(label)
            note_obj = Note.objects.get(id=request.data['note_id'])
            print(note_obj)
            label.note.add(note_obj)
            return Response({"message": "note and label combined"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        label = Label.objects.get(id=request.data['id'])
        # print(label)
        # note = label.note.all() | Note.objects.filter(id=request.data['id'])
        note = Note.objects.get(id=16)
        print(label.note.all())
        print(note.label_set.all())
        # print([i for i in note])

        # request_data = request.data
        # print(request_data)
        # label_name = request_data.get("title")
        # label_data = Label.objects.get(title=label_name)
        # print(label_data)
        # note_data = label_data.note.all()
        # print(note_data)
        # note = Note.objects.filter(user_id=request_data["user_id"])
        # print(note.note.all())
        return Response({"message": "user found"},
                        status=status.HTTP_200_OK)


class Collaborator(APIView):

    @verify_token
    def post(self, request):
        try:
            note = Note.objects.get(id=request.data['id'])
            user = User.objects.get(id=request.data['user_id'])
            user.collaborator.add(note)
            return Response({"message": "collaborated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        try:
            user = User.objects.get(id=request.data['user_id'])
            note = user.collaborator.all() | Note.objects.filter(user_id=request.data['user_id'])
            print([i for i in note])
            return Response({"message": "user found", "data": NoteSerializer(note, many=True).data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
