import logging

from rest_framework.response import Response
from rest_framework import generics, mixins

from .models import Note
from .serializers import NoteSerializer

logging.basicConfig(filename="view.log", filemode="w")


class NoteView(generics.ListCreateAPIView):
    """
        Creating note view and performing crud operation
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class NoteDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def update(self, request, *args, **kwargs):
        pk = request.data.get('id')
        queryset = self.get_queryset().get(pk=pk)
        serializer = self.serializer_class(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        querysert = self.get_queryset().get(pk=kwargs.get('pk'))
        serilizer = self.serializer_class(querysert)
        print(serilizer.data)
        return Response(serilizer.data)

    def destroy(self, request, *args, **kwargs):
        pk = request.data.get('id')
        del (pk)
        return Response({"message": 'note deleted'})


# class NoteDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     lookup_field = "pk"
#     def get(self, request, *args, **kwargs):
#         pk = request.data.get('id')
#         kwargs['pk']=pk
#         return self.retrieve(request, *args, **kwargs)
