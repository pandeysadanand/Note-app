from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


def index(request):
    return HttpResponse("This is my first real time project")


class Signup(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': serializer.errors})
            serializer.save()
            return Response({'data': serializer.data})
        except Exception as e:
            return Response({'message': str(e)})


class Login(APIView):
    def post(self, request):
        try:
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
            if user is not None:
                return Response({"message": "successfully login"})
            else:
                return Response({"message": "login error"})
        except Exception as e:
            return Response({"message": str(e)})
