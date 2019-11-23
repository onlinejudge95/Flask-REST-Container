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
    assert (
        "User with email onlinejudge95@gmail.com already exists"
        in data["message"]
    )


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
    assert "User with id 123 does not exists" in data["message"]


def test_get_users(test_app, test_database):
    utils.recreate_db()
    utils.add_user(
        {"username": "mayankdcoder", "email": "mayankdcoder@gmail.com"}
    )
    utils.add_user(
        {"username": "mayankdcoder1", "email": "mayankdcoder1@gmail.com"}
    )

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


def test_remove_user(test_app, test_database):
    utils.recreate_db()
    public_id = utils.add_user(
        {"username": "removed", "email": "remove@gmail.com"}
    )
    client = test_app.test_client()
    resp_one = client.get("/users")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data["data"]["users"]) == 1
    resp_two = client.delete(f"/users/{public_id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "remove@gmail.com was removed!" in data["message"]
    assert "success" in data["status"]
    resp_three = client.get("/users")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data["data"]["users"]) == 0


def test_remove_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User with id 999 does not exists" in data["message"]
    assert "fail" in data["status"]


def test_update_user(test_app, test_database):
    utils.recreate_db()
    public_id = utils.add_user(
        {"username": "update", "email": "update@gmail.com"}
    )
    client = test_app.test_client()
    resp_one = client.put(
        f"/users/{public_id}",
        data=json.dumps({"username": "me", "email": "me@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{public_id} was updated!" in data["message"]
    assert "success" in data["status"]
    resp_two = client.get(f"/users/{public_id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "me" in data["data"]["username"], data["data"]
    assert "me@gmail.com" in data["data"]["email"]
    assert "success" in data["status"]


def test_update_user_wrong_permission(test_app, test_database):
    utils.recreate_db()
    public_id = utils.add_user(
        {"username": "update", "email": "update@gmail.com"}
    )
    client = test_app.test_client()
    resp = client.put(
        f"/users/{public_id}",
        data=json.dumps({"public_id": "123"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 403
    assert "Can not modify public_id attribute" in data["message"]
    assert "fail" in data["status"]


def test_update_user_does_not_exist(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/users/999",
        data=json.dumps({"username": "me", "email": "me@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User with id 999 does not exists" in data["message"]
    assert "fail" in data["status"]


def test_update_user_empty_json(test_app, test_database):
    utils.recreate_db()
    public_id = utils.add_user(
        {"username": "update", "email": "update@gmail.com"}
    )
    client = test_app.test_client()
    resp = client.put(
        f"/users/{public_id}",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Empty payload" in data["message"]
    assert "fail" in data["status"]
