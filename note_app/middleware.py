import logging

from rest_framework.utils import json

from user.models import User, LoginData


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_exception(self, request, exception):
        logging.exception(exception)

    def __call__(self, request):

        response = self.get_response(request)
        try:
            print(request.path)
            if '/user/login' in request.path:
                request_dict = json.loads(request.body)
                user = User.objects.get(username=request_dict.get("username"))
                LoginData.objects.create(user_id_id=user.pk, token=response.data['token'])
        except Exception as e:
            logging.exception(e)
        return response
