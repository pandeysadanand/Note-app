import json
import logging
from functools import wraps

from rest_framework.response import Response

from note.serializers import LabelSerializer
from note_app.redis_service import RedisService
from user.utils import EncodeDecode

logging.basicConfig(filename="view.log", filemode="w")


# logger = logging.getLogger(__name__)


def verify_token(function):
    """
        creating function to verify token
    """

    @wraps(function)
    def wrapper(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            response = Response({"message": 'Token not provided in the header'})
            response.status_code = 401
            logging.info('Token not provided in the header')
            return response
        token = request.META['HTTP_AUTHORIZATION']
        id = EncodeDecode().decode_token(token)
        request.data.update({'user_id': id.get("user_id")})
        return function(self, request)

    return wrapper


def get_note_format(note_data):
    note_list = []
    for note in note_data:
        note_labels = note.label_set.all()
        note_list.append({
            "note_id": note.id,
            "title": note.title,
            "description": note.description,
            "color": note.color,
            "archive": note.archive,
            "label_list": LabelSerializer(note_labels, many=True).data
        })

    return note_list


class RedisOperation:
    def __init__(self):
        self.redis_object = RedisService()

    def get_notes(self, user_id):
        """
        for getting note from cache
        :param user_id: user_id
        :return:
        """
        try:
            data = self.redis_object.get(int(user_id))
            print(data)
            if data is None:
                return []
            data_list = [item for _, item in json.loads(data).items()]
            return data_list
        except Exception as e:
            logging.error(e)

    def add_note(self, user_id, note):
        try:
            data = self.redis_object.get(user_id)
            if not data:
                data = json.dumps({})
            data_dict = json.loads(data)
            data_dict.update({str(note.get('id')): note})
            self.redis_object.set(user_id, json.dumps(data_dict))
        except Exception as e:
            logging.error(e)

    def update_notes(self, note, user_id):
        """
        updating existing note to cache
        :param note: note details
        :param user_id: user id of logged user
        :return: none
        """
        try:

            id = str(note.get('id'))
            note_dict = json.loads(self.redis_object.get(user_id))
            if note_dict.get(id):
                note_dict.update({id: note})
                self.redis_object.set(user_id, json.dumps(note_dict))
        except Exception as e:
            logging.error(e)

    def delete_notes(self, user_id, note_id):
        """
        deleting note from cache
        :param user_id: user_id of logged user
        :param note_id: note details
        :return: none
        """
        try:
            data = self.redis_object.get(user_id)
            if data:
                note_list = json.loads(data)
                if note_list.get(str(note_id)):
                    note_list.pop(str(note_id))
                    self.redis_object.set(user_id, json.dumps(note_list))
        except Exception as e:
            logging.error(e)
