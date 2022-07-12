import pytest
from rest_framework.reverse import reverse

from note.models import Note

NOTE_URL = reverse('note_api')

@pytest.fixture
def create_user(django_user_model, db):
    return django_user_model.objects.create_user(username="sadanand", email="email@gmail.com", password="email@123")


@pytest.fixture
def headers(create_user, client, db):
    payload = {
        'username': "sadanand",
        'password': "email@123",
    }
    response = client.post(reverse('login_api'), payload)
    token=  response.data['data']['token']
    return {'HTTP_AUTHORIZATION': token, 'content_type': 'application/json'}


class TestNote:

    def test_note_cannot_register_with_no_data(self, client, headers):
        res = client.post(NOTE_URL, **headers)
        assert res.status_code == 400

    def test_note_create_correctly(self, client, db, create_user, headers):
        note_data = {
            'user_id': create_user.id,
            'title': "java",
            'color': "red",
            'description': "This is new notes",
            'is_archive': True,
        }
        response = client.post(NOTE_URL, note_data, **headers)

        assert response.data['data']['user_id'] == create_user.id
        assert response.data['data']['title'] == note_data['title']
        assert response.data['data']['color'] == note_data['color']
        assert response.data['data']['description'] == note_data['description']
        assert response.status_code == 201

    def test_note_update_correctly(self, client, db, create_user, headers):
        note_data = {
            'title': "java",
            'color': "red",
            'description': "This is new notes",
            'is_archive': True,
        }

        res = client.post(NOTE_URL, note_data, **headers)
        note_id = res.data['data']['id']
        updated_note_data = {
            'note_id': note_id,
            'title': "python",
            'color': "black",
            'description': "This is new notes",
            'is_archive': True,
        }
        response = client.put(NOTE_URL, updated_note_data, **headers)
        assert response.data['data']['title'] == updated_note_data.get('title')
        assert response.status_code == 202

    def test_note_delete_correctly(self, client, db, create_user, headers):
        note_data = {
            'title': "java",
            'color': "red",
            'description': "This is new notes",
            'is_archive': True,
        }

        response = client.post(NOTE_URL, note_data, **headers)
        note_id = response.data['data']['id']
        res = client.delete(NOTE_URL, {'note_id': note_id}, **headers)

        assert res.status_code == 204

    def test_note_get_correctly(self, client, db, create_user, headers):
        note_data = {
            'title': "java",
            'color': "red",
            'description': "This is new notes",
            'is_archive': True,
        }
        response = client.post(NOTE_URL, note_data, **headers)
        note_id = response.data['data']['id']

        response = client.delete(NOTE_URL, {"note_id": note_id}, **headers)
        assert Note.objects.count() == 0
        assert response.status_code == 204
