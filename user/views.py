import logging

from django.contrib import auth
from django.http import HttpResponse
from jwt import ExpiredSignatureError, DecodeError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
from .utils import EncodeDecode
from user.tasks import send_email
logging.basicConfig(filename="view.log", filemode="w")


def index(request):
    return HttpResponse("This is my first real time project")


class Signup(APIView):

    def post(self, request):
        """
            Registering new user with name, phone location, email
        """
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = EncodeDecode().encode_token({"id": serializer.data.get('id')})
            # url = "http://127.0.0.1:8000/user/validate/" + str(token)
            send_email.delay(token=str(token), email=serializer.data['email'])
            # send_mail.delay("register", url, settings.EMAIL_HOST_USER, [serializer.data['email']], fail_silently=False)
            return Response({"message": "data store successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        """
            login existing user with username and password
        """
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                token = EncodeDecode().encode_token(payload={"user_id": user.pk})
                return Response({"message": "login successful", "data": {"token": token}}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "user login unsuccessful", "data": {}}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    def get(self, request, token):
        """
            Checking existing token whether it is valid or expired
        """
        try:
            decode_token = EncodeDecode().decode_token(token=token)
            user = User.objects.get(id=decode_token.get('id'))
            user.is_verified = True
            user.save()
            return Response({"message": "Validate Successfully", "data": user.pk},
                            status=status.HTTP_201_CREATED)
        except ExpiredSignatureError:
            return Response({"message": "token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except DecodeError:
            return Response({"message": "wrong token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# todo reddish server, cashing data . install reddish server, python reddish pakg[set and get]
# key = user_id value=dic 0f note_id[note_details]
# reddish cll->