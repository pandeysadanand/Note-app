from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status
from .serializers import UserSerializer


def index(request):
    return HttpResponse("This is my first real time project")


class Signup(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        try:
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
            if user:
                return Response({"message": "successfully login"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "login error"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
