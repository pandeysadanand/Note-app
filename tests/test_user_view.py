import pytest
from faker import Faker
from rest_framework.reverse import reverse

from note.models import Note
from user.models import User

faker = Faker()
REGISTER_URL = reverse('register_api')
LOGIN_URL = reverse('login_api')


@pytest.fixture
def create_user():
    return User.objects.create_user(username="sadanand", email="email@gmail.com", password="email@123")


class TestUser:

    def test_user_cannot_register_with_no_data(self, client):
        res = client.post(REGISTER_URL)
        assert res.status_code == 400

    def test_user_register_correctly(self, client, db):
        user_data = {
            'email': "email@gmail.com",
            'username': "pandey",
            'password': "pandey@123",
        }
        res = client.post(REGISTER_URL, user_data, format="json")
        assert res.data['data']['email'] == user_data['email']
        assert res.data['data']['username'] == user_data['username']
        assert res.status_code == 201

    def test_user_login_fail(self, client):
        user_data = {
            'email': faker.email(),
            'username': faker.user_name(),
            'password': faker.password(),
        }
        client.post(REGISTER_URL, user_data, format="json")
        # user_data['username'] = ""
        del user_data['username']
        user_data['password'] = ""
        res = client.post(LOGIN_URL, user_data, format="json")
        assert res.status_code == 401

    def test_user_login_successful(self, client, db):
        user_data = {
            'email': faker.email(),
            'username': faker.user_name(),
            'password': faker.password(),
        }
        client.post(REGISTER_URL, user_data, format="json")
        del user_data['email']
        res = client.post(LOGIN_URL, user_data, format="json")
        assert res.status_code == 200


NOTE_URL = reverse('note_api')


class TestNote:
    def test_note_cannot_register_with_no_data(self, client):
        res = client.post(NOTE_URL)
        assert res.status_code == 400

    def test_note_create_correctly(self, client, db, create_user):
        note_data = {
            'user_id': create_user.id,
            'title': "java",
            'color': "red",
            'description': "This is new notes",
            'is_archive': True,
        }
        response = client.post(NOTE_URL, note_data, format="json")

        assert response.data['data']['user_id'] == create_user.id
        assert response.data['data']['title'] == note_data['title']
        assert response.data['data']['color'] == note_data['color']
        assert response.data['data']['description'] == note_data['description']
        assert response.status_code == 201

    def test_note_update_correctly(self, client, db, create_user):
        note_data = {
            'user_id': create_user.id,
            'title': "java",
            'color': "red",
            'description': "This is new notes",
            'is_archive': True,
        }

        res = client.post(NOTE_URL, note_data, format="json")
        print(res.data)
        updated_note_data = {
            'note_id': res.data['data']['id'],
            'user_id': create_user.id,
            'title': "python",
            'color': "black",
            'description': "This is new notes",
            'is_archive': True,
        }
        print(res.data['data']['id'])
        response = client.put(reverse('note_api', args=[res.data['data']['id']]), format="json")
        print(response.status_code)
        assert response.data['data']['title'] == updated_note_data.get('title')
        assert response.status_code == 200

    def test_note_delete_correctly(self, client, db, create_user):
        note_data = {
            'user_id': create_user.id,
            'title': "java",
            'color': "red",
            'description': "This is new notes",
            'is_archive': True,
        }

        response = client.post(NOTE_URL, note_data, format="json")

        res = client.delete(reverse('note_api', args=[response.data['data']['id']]), response)

        assert res.status_code == 204

    def test_note_get_correctly(self, client, db, create_user):
        note_data = {
            'user_id': create_user.id,
            'title': "java",
            'color': "red",
            'description': "This is new notes",
            'is_archive': True,
        }
        response = client.post(NOTE_URL, note_data, format="json")
        url = reverse('note_api', args=[response.data['data']['id']])
        response = client.delete(url, CONTENT_TYPE='application/json')
        assert Note.objects.count() == 0
        assert response.status_code == 204
