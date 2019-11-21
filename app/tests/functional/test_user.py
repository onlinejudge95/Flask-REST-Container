import json

from app import utils


def test_add_user(test_app, test_database):
    client = test_app.test_client()

    response = client.post(
        "/users",
        data=json.dumps(
            {"username": "onlinejudge95", "email": "onlinejudge95@gmail.com",}
        ),
        content_type="application/json",
    )
    assert response.status_code == 201

    data = json.loads(response.data.decode())
    assert "success" in data["status"]
    assert "onlinejudge95@gmail.com was added!" in data["message"]
    assert "public_id" in data["data"].keys()


def test_add_user_empty_data(test_app, test_database):
    client = test_app.test_client()

    response = client.post(
        "/users", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400

    data = json.loads(response.data.decode())
    assert "fail" in data["status"]
    assert "Empty payload" in data["message"]


def test_add_user_invalid_payload(test_app, test_database):
    client = test_app.test_client()

    response = client.post(
        "/users",
        data=json.dumps({"email": "mayankdcoder@gmail.com"}),
        content_type="application/json",
    )
    assert response.status_code == 400

    data = json.loads(response.data.decode())
    assert "fail" in data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()

    client.post(
        "/users",
        data=json.dumps(
            {"username": "onlinejudge95", "email": "onlinejudge95@gmail.com"}
        ),
        content_type="application/json",
    )

    response = client.post(
        "/users",
        data=json.dumps(
            {"username": "onlinejudge95", "email": "onlinejudge95@gmail.com"}
        ),
        content_type="application/json",
    )
    assert response.status_code == 400

    data = json.loads(response.data.decode())
    assert "fail" in data["status"]
    assert "Sorry. That email already exists." in data["message"]


def test_get_user(test_app, test_database):
    public_id = utils.add_user(
        {"username": "onlinejudge95", "email": "onlinejudge95@gmail.com"}
    )
    client = test_app.test_client()

    response = client.get(f"/users/{public_id}")
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert "success" in data["status"]
    assert "onlinejudge95" in data["data"]["username"], data["data"]
    assert "onlinejudge95@gmail.com" in data["data"]["email"]


def test_get_user_invalid_id(test_app, test_database):
    client = test_app.test_client()

    response = client.get("/users/123")
    assert response.status_code == 404

    data = json.loads(response.data.decode())
    assert "fail" in data["status"]
    assert "User does not exist" in data["message"]


def test_get_users(test_app, test_database):
    utils.recreate_db()
    utils.add_user({"username": "mayankdcoder", "email": "mayankdcoder@gmail.com"})
    utils.add_user({"username": "mayankdcoder1", "email": "mayankdcoder1@gmail.com"})

    client = test_app.test_client()

    response = client.get("/users")
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert "success" in data["status"]
    assert len(data["data"]["users"]) == 2
    assert "mayankdcoder" in data["data"]["users"][0]["username"]
    assert "mayankdcoder1" in data["data"]["users"][1]["username"]
    assert "mayankdcoder@gmail.com" in data["data"]["users"][0]["email"]
    assert "mayankdcoder1@gmail.com" in data["data"]["users"][1]["email"]
