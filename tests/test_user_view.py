import pytest
from faker import Faker
from rest_framework.reverse import reverse

from note.models import Note
from user.models import User

faker = Faker()
REGISTER_URL = reverse('register_api')
LOGIN_URL = reverse('login_api')


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
        res = client.post(REGISTER_URL, user_data)
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
