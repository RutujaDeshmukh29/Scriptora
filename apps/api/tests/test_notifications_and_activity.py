"""
Tests that notifications and activity log entries are actually triggered by
the actions that should cause them — not just that the endpoints exist.
"""


def _register_and_login(client, email: str, name: str = "Test User"):
    response = client.post(
        "/api/v1/auth/register", json={"name": name, "email": email, "password": "correct-horse-battery"}
    )
    assert response.status_code == 201
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_creating_project_logs_activity(client):
    owner_token = _register_and_login(client, "activityowner1@example.com")
    project = client.post("/api/v1/projects", json={"name": "Logged Project"}, headers=_auth_headers(owner_token)).json()

    activity = client.get(f"/api/v1/projects/{project['id']}/activity", headers=_auth_headers(owner_token)).json()
    action_types = [entry["action_type"] for entry in activity]
    assert "project_created" in action_types


def test_creating_script_logs_activity(client):
    owner_token = _register_and_login(client, "activityowner2@example.com")
    project = client.post("/api/v1/projects", json={"name": "Script Activity Project"}, headers=_auth_headers(owner_token)).json()
    client.post(f"/api/v1/projects/{project['id']}/scripts", json={"title": "Pilot"}, headers=_auth_headers(owner_token))

    activity = client.get(f"/api/v1/projects/{project['id']}/activity", headers=_auth_headers(owner_token)).json()
    script_events = [e for e in activity if e["action_type"] == "script_created"]
    assert len(script_events) == 1
    assert script_events[0]["extra_data"]["title"] == "Pilot"


def test_autosave_does_not_spam_activity_log(client):
    """Explicitly verifies the deliberate scope cut — autosave is NOT logged."""
    owner_token = _register_and_login(client, "activityowner3@example.com")
    project = client.post("/api/v1/projects", json={"name": "Autosave Project"}, headers=_auth_headers(owner_token)).json()
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Draft"}, headers=_auth_headers(owner_token)
    ).json()

    # Simulate several autosave ticks
    for i in range(5):
        client.patch(f"/api/v1/scripts/{script['id']}", json={"content": f"revision {i}"}, headers=_auth_headers(owner_token))

    activity = client.get(f"/api/v1/projects/{project['id']}/activity", headers=_auth_headers(owner_token)).json()
    edit_events = [e for e in activity if e["action_type"] == "script_edited"]
    assert len(edit_events) == 0
    # Only the single script_created event should be there, not 5 edit events
    assert len([e for e in activity if e["action_type"] == "script_created"]) == 1


def test_inviting_member_creates_notification_and_activity(client):
    owner_token = _register_and_login(client, "activityowner4@example.com")
    invitee_token = _register_and_login(client, "invitee1@example.com")
    project = client.post("/api/v1/projects", json={"name": "Invite Notif Project"}, headers=_auth_headers(owner_token)).json()

    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "invitee1@example.com", "role": "editor"},
        headers=_auth_headers(owner_token),
    )

    # The invited user should have a notification
    notifications = client.get("/api/v1/notifications", headers=_auth_headers(invitee_token)).json()
    invite_notifs = [n for n in notifications if n["type"] == "project_invite"]
    assert len(invite_notifs) == 1
    assert invite_notifs[0]["payload"]["project_name"] == "Invite Notif Project"
    assert invite_notifs[0]["read"] is False

    # And the project's activity log should show it
    activity = client.get(f"/api/v1/projects/{project['id']}/activity", headers=_auth_headers(owner_token)).json()
    assert any(e["action_type"] == "member_joined" for e in activity)


def test_commenting_notifies_script_creator_but_not_self(client):
    owner_token = _register_and_login(client, "scriptcreator1@example.com")
    commenter_token = _register_and_login(client, "commenter1@example.com")
    project = client.post("/api/v1/projects", json={"name": "Comment Notif Project"}, headers=_auth_headers(owner_token)).json()
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "commenter1@example.com", "role": "editor"},
        headers=_auth_headers(owner_token),
    )
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "Commented Script"}, headers=_auth_headers(owner_token)
    ).json()

    # A different user comments on the owner's script
    client.post(
        f"/api/v1/scripts/{script['id']}/comments", json={"content": "Nice work"}, headers=_auth_headers(commenter_token)
    )

    owner_notifications = client.get("/api/v1/notifications", headers=_auth_headers(owner_token)).json()
    assert any(n["type"] == "new_comment" for n in owner_notifications)

    # The commenter should NOT notify themselves
    commenter_notifications = client.get("/api/v1/notifications", headers=_auth_headers(commenter_token)).json()
    assert not any(n["type"] == "new_comment" for n in commenter_notifications)


def test_commenting_on_own_script_does_not_self_notify(client):
    owner_token = _register_and_login(client, "selfcommenter1@example.com")
    project = client.post("/api/v1/projects", json={"name": "Self Comment Project"}, headers=_auth_headers(owner_token)).json()
    script = client.post(
        f"/api/v1/projects/{project['id']}/scripts", json={"title": "My Own Script"}, headers=_auth_headers(owner_token)
    ).json()

    client.post(
        f"/api/v1/scripts/{script['id']}/comments", json={"content": "note to self"}, headers=_auth_headers(owner_token)
    )

    notifications = client.get("/api/v1/notifications", headers=_auth_headers(owner_token)).json()
    assert not any(n["type"] == "new_comment" for n in notifications)


def test_mark_notification_read(client):
    owner_token = _register_and_login(client, "activityowner5@example.com")
    invitee_token = _register_and_login(client, "invitee2@example.com")
    project = client.post("/api/v1/projects", json={"name": "Read Notif Project"}, headers=_auth_headers(owner_token)).json()
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "invitee2@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )

    notifications = client.get("/api/v1/notifications", headers=_auth_headers(invitee_token)).json()
    notif_id = notifications[0]["id"]

    response = client.patch(f"/api/v1/notifications/{notif_id}/read", headers=_auth_headers(invitee_token))
    assert response.status_code == 200
    assert response.json()["read"] is True


def test_cannot_read_another_users_notification(client):
    owner_token = _register_and_login(client, "activityowner6@example.com")
    invitee_token = _register_and_login(client, "invitee3@example.com")
    stranger_token = _register_and_login(client, "notifstranger1@example.com")
    project = client.post("/api/v1/projects", json={"name": "Isolation Project"}, headers=_auth_headers(owner_token)).json()
    client.post(
        f"/api/v1/projects/{project['id']}/members",
        json={"email": "invitee3@example.com", "role": "viewer"},
        headers=_auth_headers(owner_token),
    )

    notifications = client.get("/api/v1/notifications", headers=_auth_headers(invitee_token)).json()
    notif_id = notifications[0]["id"]

    response = client.patch(f"/api/v1/notifications/{notif_id}/read", headers=_auth_headers(stranger_token))
    assert response.status_code == 404


def test_activity_requires_project_membership(client):
    owner_token = _register_and_login(client, "activityowner7@example.com")
    stranger_token = _register_and_login(client, "activitystranger1@example.com")
    project = client.post("/api/v1/projects", json={"name": "Private Activity Project"}, headers=_auth_headers(owner_token)).json()

    response = client.get(f"/api/v1/projects/{project['id']}/activity", headers=_auth_headers(stranger_token))
    assert response.status_code == 404
