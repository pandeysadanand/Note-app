import logging

from django.contrib import auth
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from jwt import ExpiredSignatureError, DecodeError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .producer import RabbitServer
from .serializers import UserSerializer
from .utils import EncodeDecode
from user.tasks import send_email_task
logging.basicConfig(filename="view.log", filemode="w")


def index(request):
    return HttpResponse("This is my first real time project")


class Signup(APIView):
    """class based view for registration"""

    @swagger_auto_schema(
        operation_summary="registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='phone'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='location'),
            }
        ))
    def post(self, request):
        """
            Registering new user with name, phone location, email
            :param request: username and password
            :return: returning message and data
        """
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = EncodeDecode().encode_token({"id": serializer.data.get('id')})
            RabbitServer().send_message(serializer.data)
            send_email_task.delay(token=str(token), email=serializer.data['email'])
            # send_email_task(token=str(token), email=serializer.data['email'])
            return Response({"message": "data store successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="display",
    )
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class Login(APIView):
    """class based views for user login"""

    @swagger_auto_schema(
        operation_summary="login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            }
        ))
    def post(self, request):
        """
            login existing user with username and password
            param request: username and password
            return:response
        """
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                token = EncodeDecode().encode_token(payload={"user_id": user.pk})
                return Response({"message": "login successful", "data": {"token": token}}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "user login unsuccessful", "data": {}}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    """class based views for token validation"""

    @swagger_auto_schema(
        operation_summary="get user"
    )
    def get(self, request, token):
        """
        this method is use for get token
        :param request:
        :param token:
        :return:response
        """
        try:
            decode_token = EncodeDecode().decode_token(token=token)
            user = User.objects.get(id=decode_token.get('id'))
            user.is_verified = True
            user.save()
            serializer = UserSerializer(user)
            return Response({"message": "Validate Successfully"},
                            status=status.HTTP_201_CREATED)
        except ExpiredSignatureError:
            return Response({"message": "token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except DecodeError:
            return Response({"message": "wrong token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

