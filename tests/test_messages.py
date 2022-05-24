from tests import utils


def test_post_message(client):
    response = utils.post_message(
        client, "sergio", "guido", "hola soy sergio [REDACTED]"
    )
    assert response.status_code == 200
    assert response.json()["text"] == "hola soy sergio [REDACTED]"
    assert response.json()["sender"]["id"] == "sergio"
    assert response.json()["receiver"]["id"] == "guido"


def test_get_messages_with_zero_messages(client):
    response = utils.get_messages(client, "sergio", "guido")
    assert response.status_code == 200
    assert response.json() == []


def test_get_messages_creates_user_with_id_uid_if_not_exists(client):
    utils.post_message(client, "sergio", "guido", "hola soy sergio [REDACTED]")

    response = utils.get_messages(client, "does_not_exist", "guido")
    messages = response.json()

    assert response.status_code == 200
    assert len(messages) == 0


def test_get_messages_creates_user_with_id_other_if_not_exists(client):
    utils.post_message(client, "sergio", "guido", "hola soy sergio [REDACTED]")

    response = utils.get_messages(client, "sergio", "does_not_exist")
    messages = response.json()

    assert response.status_code == 200
    assert len(messages) == 0


def test_get_messages_with_one_message(client):
    message_id = utils.post_message(
        client, "sergio", "guido", "hola soy sergio [REDACTED]"
    ).json()["id"]

    response = utils.get_messages(client, "sergio", "guido")
    messages = response.json()

    assert response.status_code == 200
    assert len(messages) == 1
    assert messages[0]["id"] == message_id
    assert messages[0]["text"] == "hola soy sergio [REDACTED]"
    assert messages[0]["sender"]["id"] == "sergio"
    assert messages[0]["receiver"]["id"] == "guido"


def test_get_messages_with_many_messages(client):
    utils.post_message(client, "sergio", "guido", "hola soy sergio [REDACTED]")
    utils.post_message(client, "sergio", "guido", "falta la [REDACTED]")
    utils.post_message(client, "sergio", "guido", "eso es detalle de [REDACTED]")

    response = utils.get_messages(client, "sergio", "guido")
    messages = response.json()

    assert response.status_code == 200
    assert len(messages) == 3
    assert messages[0]["text"] == "hola soy sergio [REDACTED]"
    assert messages[1]["text"] == "falta la [REDACTED]"
    assert messages[2]["text"] == "eso es detalle de [REDACTED]"


def test_get_messages_only_returns_messages_from_conversation(client):
    utils.post_message(client, "sergio", "guido", "hola soy sergio [REDACTED]")
    utils.post_message(client, "sergio", "tomas", "punto extra para [REDACTED]")

    response = utils.get_messages(client, "sergio", "guido")
    messages = response.json()

    assert response.status_code == 200
    assert len(messages) == 1
    assert messages[0]["text"] == "hola soy sergio [REDACTED]"
    assert messages[0]["sender"]["id"] == "sergio"
    assert messages[0]["receiver"]["id"] == "guido"
    assert messages[0]["created_at"] is not None


def test_delete_message(client):
    message_id = utils.post_message(
        client, "sergio", "guido", "hola soy sergio [REDACTED]"
    ).json()["id"]

    response = utils.delete_message(client, uid="sergio", message_id=message_id)
    assert response.status_code == 200

    response = utils.get_messages(client, "sergio", "guido")
    messages = response.json()
    assert response.status_code == 200
    assert len(messages) == 0


def test_delete_invalid_message_should_fail(client):
    response = utils.delete_message(client, "sergio", 42)
    assert response.status_code == 404


def test_receiver_cannot_delete_message_from_sender(client):
    message_id = utils.post_message(
        client, "sergio", "guido", "hola soy sergio [REDACTED]"
    ).json()["id"]

    response = utils.delete_message(client, "guido", message_id)
    assert response.status_code == 403


def test_random_user_cannot_delete_message_from_sender(client):
    message_id = utils.post_message(
        client, "sergio", "guido", "hola soy sergio [REDACTED]"
    ).json()["id"]

    response = utils.delete_message(client, "tomas", message_id)
    assert response.status_code == 403