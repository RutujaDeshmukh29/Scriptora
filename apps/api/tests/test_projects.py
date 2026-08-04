"""
Tests for project CRUD and role enforcement. Two helper functions register
a user and log them in, since almost every test needs an authenticated actor.
"""


def _register_and_login(client, email: str, name: str = "Test User"):
    response = client.post(
        "/api/v1/auth/register", json={"name": name, "email": email, "password": "correct-horse-battery"}
    )
    assert response.status_code == 201
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_create_project_makes_creator_the_owner(client):
    token = _register_and_login(client, "owner1@example.com")
    response = client.post("/api/v1/projects", json={"name": "Pilot Script"}, headers=_auth_headers(token))
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Pilot Script"
    assert body["my_role"] == "owner"
    assert body["status"] == "active"


def test_list_projects_only_shows_own_projects(client):
    token_a = _register_and_login(client, "usera@example.com")
    token_b = _register_and_login(client, "userb@example.com")

    client.post("/api/v1/projects", json={"name": "A's Project"}, headers=_auth_headers(token_a))
    client.post("/api/v1/projects", json={"name": "B's Project"}, headers=_auth_headers(token_b))

    response_a = client.get("/api/v1/projects", headers=_auth_headers(token_a))
    names_a = [p["name"] for p in response_a.json()]
    assert "A's Project" in names_a
    assert "B's Project" not in names_a


def test_non_member_gets_404_not_403(client):
    """A non-member shouldn't be able to tell the project even exists."""
    owner_token = _register_and_login(client, "owner2@example.com")
    stranger_token = _register_and_login(client, "stranger@example.com")

    project = client.post(
        "/api/v1/projects", json={"name": "Private Project"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.get(f"/api/v1/projects/{project['id']}", headers=_auth_headers(stranger_token))
    assert response.status_code == 404


def test_owner_can_invite_existing_user_as_editor(client):
    owner_token = _register_and_login(client, "owner3@example.com")
    _register_and_login(client, "editor1@example.com")  # must exist first — no email-invite flow yet

    project = client.post(
        "/api/v1/projects", json={"name": "Team Project"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "editor1@example.com", "role": "editor"},
        headers=_auth_headers(owner_token),
    )
    assert response.status_code == 201
    assert response.json()["role"] == "editor"
    assert response.json()["user"]["email"] == "editor1@example.com"


def test_inviting_unregistered_email_fails_clearly(client):
    owner_token = _register_and_login(client, "owner4@example.com")
    project = client.post(
        "/api/v1/projects", json={"name": "Solo Project"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "nobody.registered@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )
    assert response.status_code == 404


def test_editor_cannot_manage_members(client):
    owner_token = _register_and_login(client, "owner5@example.com")
    editor_token = _register_and_login(client, "editor2@example.com")

    project = client.post(
        "/api/v1/projects", json={"name": "Guarded Project"}, headers=_auth_headers(owner_token)
    ).json()
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "editor2@example.com", "role": "editor"},
        headers=_auth_headers(owner_token),
    )

    # editor tries to invite someone else — must be rejected
    _register_and_login(client, "viewer1@example.com")
    response = client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "viewer1@example.com", "role": "viewer"},
        headers=_auth_headers(editor_token),
    )
    assert response.status_code == 403


def test_editor_cannot_update_project_settings(client):
    owner_token = _register_and_login(client, "owner6@example.com")
    editor_token = _register_and_login(client, "editor3@example.com")

    project = client.post(
        "/api/v1/projects", json={"name": "Locked Settings"}, headers=_auth_headers(owner_token)
    ).json()
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "editor3@example.com", "role": "editor"},
        headers=_auth_headers(owner_token),
    )

    response = client.patch(
        f"/api/v1/projects/{project['id']}",
        json={"name": "Renamed By Editor"},
        headers=_auth_headers(editor_token),
    )
    assert response.status_code == 403


def test_viewer_can_still_view_project(client):
    owner_token = _register_and_login(client, "owner7@example.com")
    viewer_token = _register_and_login(client, "viewer2@example.com")

    project = client.post(
        "/api/v1/projects", json={"name": "Viewable Project"}, headers=_auth_headers(owner_token)
    ).json()
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "viewer2@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )

    response = client.get(f"/api/v1/projects/{project['id']}", headers=_auth_headers(viewer_token))
    assert response.status_code == 200
    assert response.json()["my_role"] == "viewer"


def test_cannot_remove_the_last_owner(client):
    owner_token = _register_and_login(client, "soleowner@example.com")
    project = client.post(
        "/api/v1/projects", json={"name": "Solo Owned"}, headers=_auth_headers(owner_token)
    ).json()

    # Need the owner's own user id — fetch it via /me
    me = client.get("/api/v1/auth/me", headers=_auth_headers(owner_token)).json()

    response = client.delete(
        f"/api/v1/projects/{project['id']}/members/{me['id']}", headers=_auth_headers(owner_token)
    )
    assert response.status_code == 409


def test_owner_can_remove_a_non_owner_member(client):
    owner_token = _register_and_login(client, "owner8@example.com")
    _register_and_login(client, "removable@example.com")

    project = client.post(
        "/api/v1/projects", json={"name": "Removable Member Project"}, headers=_auth_headers(owner_token)
    ).json()
    add_response = client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "removable@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )
    removable_user_id = add_response.json()["user_id"]

    response = client.delete(
        f"/api/v1/projects/{project['id']}/members/{removable_user_id}", headers=_auth_headers(owner_token)
    )
    assert response.status_code == 204

    members = client.get(f"/api/v1/projects/{project['id']}/members", headers=_auth_headers(owner_token)).json()
    assert all(m["user_id"] != removable_user_id for m in members)


def test_archive_project_changes_status(client):
    owner_token = _register_and_login(client, "owner9@example.com")
    project = client.post(
        "/api/v1/projects", json={"name": "To Be Archived"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.post(f"/api/v1/projects/{project['id']}/archive", headers=_auth_headers(owner_token))
    assert response.status_code == 200
    assert response.json()["status"] == "archived"


def test_unauthenticated_request_is_rejected(client):
    response = client.get("/api/v1/projects")
    assert response.status_code == 401
