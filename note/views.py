import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import mixins

from .models import Note
from .serializers import NoteSerializer

logging.basicConfig(filename="view.log", filemode="w")


class NoteView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
        Creating note view and performing crud operation
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="get note by user_id")
    def get(self, request, *args, **kwargs):
        # note = Note.objects.filter(user_id=request.data.get('user_id'))
        # serializer = NoteView.serilizer_class(note, many=True)
        # return Response({"message": "note found", "data": serializer.data}, status=status.HTTP_200_OK)
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Update notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="color"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="delete note",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="id"),
            }
        ))
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('AUTHORIZATION', openapi.IN_HEADER, type=openapi.TYPE_STRING)
    ], operation_summary="Add notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="color"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

