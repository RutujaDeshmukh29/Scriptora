"""Tests for comments, replies, and resolve/reopen — all with inherited project-role checks."""


def _register_and_login(client, email: str, name: str = "Test User"):
    response = client.post(
        "/api/v1/auth/register", json={"name": name, "email": email, "password": "correct-horse-battery"}
    )
    assert response.status_code == 201
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _setup_project_and_script(client, owner_token: str):
    project = client.post("/api/v1/projects", json={"name": "Comment Test Project"}, headers=_auth_headers(owner_token)).json()
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Test Script"}, headers=_auth_headers(owner_token)
    ).json()
    return project, script


def test_owner_can_add_comment_with_anchor(client):
    owner_token = _register_and_login(client, "commentowner1@example.com")
    _, script = _setup_project_and_script(client, owner_token)

    response = client.post(
        f"/api/v1/scripts/{script['id']}/comments",
        json={"content": "Nice line here", "anchor_from": 5, "anchor_to": 20, "quoted_text": "the pond scene"},
        headers=_auth_headers(owner_token),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["content"] == "Nice line here"
    assert body["quoted_text"] == "the pond scene"
    assert body["resolved"] is False
    assert body["author"]["email"] == "commentowner1@example.com"
    assert body["replies"] == []


def test_viewer_cannot_add_comment(client):
    owner_token = _register_and_login(client, "commentowner2@example.com")
    viewer_token = _register_and_login(client, "commentviewer1@example.com")
    project, script = _setup_project_and_script(client, owner_token)
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "commentviewer1@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )

    response = client.post(
        f"/api/v1/scripts/{script['id']}/comments",
        json={"content": "Should fail"},
        headers=_auth_headers(viewer_token),
    )
    assert response.status_code == 403


def test_viewer_can_read_comments(client):
    owner_token = _register_and_login(client, "commentowner3@example.com")
    viewer_token = _register_and_login(client, "commentviewer2@example.com")
    project, script = _setup_project_and_script(client, owner_token)
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "commentviewer2@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )
    client.post(
        f"/api/v1/scripts/{script['id']}/comments", json={"content": "Visible to viewer"}, headers=_auth_headers(owner_token)
    )

    response = client.get(f"/api/v1/scripts/{script['id']}/comments", headers=_auth_headers(viewer_token))
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_reply_appears_nested_under_comment(client):
    owner_token = _register_and_login(client, "commentowner4@example.com")
    _, script = _setup_project_and_script(client, owner_token)
    comment = client.post(
        f"/api/v1/scripts/{script['id']}/comments", json={"content": "Original comment"}, headers=_auth_headers(owner_token)
    ).json()

    reply_response = client.post(
        f"/api/v1/comments/{comment['id']}/replies", json={"content": "A reply"}, headers=_auth_headers(owner_token)
    )
    assert reply_response.status_code == 201
    assert reply_response.json()["content"] == "A reply"

    listing = client.get(f"/api/v1/scripts/{script['id']}/comments", headers=_auth_headers(owner_token)).json()
    assert len(listing[0]["replies"]) == 1
    assert listing[0]["replies"][0]["content"] == "A reply"


def test_editor_can_reply_but_stranger_gets_404(client):
    owner_token = _register_and_login(client, "commentowner5@example.com")
    stranger_token = _register_and_login(client, "commentstranger1@example.com")
    _, script = _setup_project_and_script(client, owner_token)
    comment = client.post(
        f"/api/v1/scripts/{script['id']}/comments", json={"content": "Private thread"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.post(
        f"/api/v1/comments/{comment['id']}/replies", json={"content": "sneaking in"}, headers=_auth_headers(stranger_token)
    )
    assert response.status_code == 404


def test_resolve_and_reopen_comment(client):
    owner_token = _register_and_login(client, "commentowner6@example.com")
    _, script = _setup_project_and_script(client, owner_token)
    comment = client.post(
        f"/api/v1/scripts/{script['id']}/comments", json={"content": "To be resolved"}, headers=_auth_headers(owner_token)
    ).json()

    resolve_response = client.patch(f"/api/v1/comments/{comment['id']}/resolve", headers=_auth_headers(owner_token))
    assert resolve_response.status_code == 200
    assert resolve_response.json()["resolved"] is True

    reopen_response = client.patch(f"/api/v1/comments/{comment['id']}/reopen", headers=_auth_headers(owner_token))
    assert reopen_response.status_code == 200
    assert reopen_response.json()["resolved"] is False


def test_viewer_cannot_resolve_comment(client):
    owner_token = _register_and_login(client, "commentowner7@example.com")
    viewer_token = _register_and_login(client, "commentviewer3@example.com")
    project, script = _setup_project_and_script(client, owner_token)
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "commentviewer3@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )
    comment = client.post(
        f"/api/v1/scripts/{script['id']}/comments", json={"content": "Locked"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.patch(f"/api/v1/comments/{comment['id']}/resolve", headers=_auth_headers(viewer_token))
    assert response.status_code == 403
