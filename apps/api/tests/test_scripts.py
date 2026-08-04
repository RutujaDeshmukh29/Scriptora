"""Tests for script CRUD and inherited project-role enforcement."""


def _register_and_login(client, email: str, name: str = "Test User"):
    response = client.post(
        "/api/v1/auth/register", json={"name": name, "email": email, "password": "correct-horse-battery"}
    )
    assert response.status_code == 201
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _create_project(client, token: str, name: str = "Test Project") -> dict:
    return client.post("/api/v1/projects", json={"name": name}, headers=_auth_headers(token)).json()


def test_owner_can_create_and_list_scripts(client):
    token = _register_and_login(client, "scriptowner1@example.com")
    project = _create_project(client, token)

    create_response = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Pilot"}, headers=_auth_headers(token)
    )
    assert create_response.status_code == 201
    assert create_response.json()["title"] == "Pilot"
    assert create_response.json()["content"] is None

    list_response = client.get(f"/api/v1/projects/{project['id']}/scripts", headers=_auth_headers(token))
    assert list_response.status_code == 200
    titles = [s["title"] for s in list_response.json()]
    assert "Pilot" in titles
    # list view should NOT include content — that's the point of ScriptSummary
    assert "content" not in list_response.json()[0]


def test_default_title_is_untitled_script(client):
    token = _register_and_login(client, "scriptowner2@example.com")
    project = _create_project(client, token)

    response = client.post(f"/api/v1/projects/{project['id']}/scripts", json={}, headers=_auth_headers(token))
    assert response.status_code == 201
    assert response.json()["title"] == "Untitled Script"


def test_viewer_cannot_create_script(client):
    owner_token = _register_and_login(client, "scriptowner3@example.com")
    viewer_token = _register_and_login(client, "scriptviewer1@example.com")
    project = _create_project(client, owner_token)
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "scriptviewer1@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )

    response = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Should fail"}, headers=_auth_headers(viewer_token)
    )
    assert response.status_code == 403


def test_viewer_can_still_read_a_script(client):
    owner_token = _register_and_login(client, "scriptowner4@example.com")
    viewer_token = _register_and_login(client, "scriptviewer2@example.com")
    project = _create_project(client, owner_token)
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "scriptviewer2@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Readable"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.get(f"/api/v1/scripts/{script['id']}", headers=_auth_headers(viewer_token))
    assert response.status_code == 200
    assert response.json()["title"] == "Readable"


def test_viewer_cannot_edit_script_content(client):
    owner_token = _register_and_login(client, "scriptowner5@example.com")
    viewer_token = _register_and_login(client, "scriptviewer3@example.com")
    project = _create_project(client, owner_token)
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "scriptviewer3@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Locked"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.patch(
        f"/api/v1/scripts/{script['id']}", json={"content": "sneaky edit"}, headers=_auth_headers(viewer_token)
    )
    assert response.status_code == 403


def test_editor_can_autosave_content(client):
    owner_token = _register_and_login(client, "scriptowner6@example.com")
    editor_token = _register_and_login(client, "scripteditor1@example.com")
    project = _create_project(client, owner_token)
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "scripteditor1@example.com", "role": "editor"},
        headers=_auth_headers(owner_token),
    )
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Draft"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.patch(
        f"/api/v1/scripts/{script['id']}",
        json={"content": "INT. OFFICE - DAY\n\nA quiet morning."},
        headers=_auth_headers(editor_token),
    )
    assert response.status_code == 200
    assert response.json()["content"] == "INT. OFFICE - DAY\n\nA quiet morning."


def test_non_member_gets_404_for_script(client):
    owner_token = _register_and_login(client, "scriptowner7@example.com")
    stranger_token = _register_and_login(client, "scriptstranger1@example.com")
    project = _create_project(client, owner_token)
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Private"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.get(f"/api/v1/scripts/{script['id']}", headers=_auth_headers(stranger_token))
    assert response.status_code == 404


def test_owner_can_delete_script(client):
    owner_token = _register_and_login(client, "scriptowner8@example.com")
    project = _create_project(client, owner_token)
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Temporary"}, headers=_auth_headers(owner_token)
    ).json()

    delete_response = client.delete(f"/api/v1/scripts/{script['id']}", headers=_auth_headers(owner_token))
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/scripts/{script['id']}", headers=_auth_headers(owner_token))
    assert get_response.status_code == 404


def test_rename_script(client):
    owner_token = _register_and_login(client, "scriptowner9@example.com")
    project = _create_project(client, owner_token)
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Old Name"}, headers=_auth_headers(owner_token)
    ).json()

    response = client.patch(
        f"/api/v1/scripts/{script['id']}", json={"title": "New Name"}, headers=_auth_headers(owner_token)
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Name"
