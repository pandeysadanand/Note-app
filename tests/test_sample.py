import pytest

from user.models import User


@pytest.mark.django_db
def test_post(client):
    # count = User.objects.count()
    response = client.get("http://127.0.0.1:8000/note/note")
    # print(dir(response))
    print(response.data)
    assert len(response.data["data"]) == 0
    # assert count == 0
