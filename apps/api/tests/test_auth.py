"""
Real, automated tests for the auth module — run with `pytest` from apps/api.
Each test gets a clean, isolated DB transaction via the `client` fixture.
"""


def test_register_creates_user_and_returns_access_token(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Rutuja", "email": "rutuja.test@example.com", "password": "correct-horse-battery"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["user"]["email"] == "rutuja.test@example.com"
    assert body["user"]["name"] == "Rutuja"
    assert "password" not in body["user"]  # never leak the hash
    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 20
    # refresh token should be set as an httpOnly cookie, not in the JSON body
    assert "refresh_token" in response.cookies
    assert "refresh_token" not in body


def test_register_rejects_duplicate_email(client):
    payload = {"name": "First", "email": "duplicate@example.com", "password": "correct-horse-battery"}
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409


def test_register_rejects_short_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Short", "email": "short@example.com", "password": "abc123"},
    )
    assert response.status_code == 422  # Pydantic min_length=8 validation


def test_login_with_correct_credentials_succeeds(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Login Test", "email": "login.test@example.com", "password": "correct-horse-battery"},
    )
    response = client.post(
        "/api/v1/auth/login", json={"email": "login.test@example.com", "password": "correct-horse-battery"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "login.test@example.com"


def test_login_with_wrong_password_fails(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Wrong PW", "email": "wrongpw@example.com", "password": "correct-horse-battery"},
    )
    response = client.post("/api/v1/auth/login", json={"email": "wrongpw@example.com", "password": "not-it"})
    assert response.status_code == 401


def test_login_with_nonexistent_email_fails(client):
    response = client.post(
        "/api/v1/auth/login", json={"email": "does.not.exist@example.com", "password": "whatever123"}
    )
    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user_with_valid_token(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={"name": "Me Test", "email": "me.test@example.com", "password": "correct-horse-battery"},
    )
    access_token = register_response.json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me.test@example.com"


def test_me_rejects_garbage_token(client):
    response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401


def test_refresh_issues_new_access_token(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Refresh Test", "email": "refresh.test@example.com", "password": "correct-horse-battery"},
    )
    # register() already set the refresh_token cookie on the client's cookie jar
    response = client.post("/api/v1/auth/refresh")
    assert response.status_code == 200
    assert len(response.json()["access_token"]) > 20


def test_refresh_token_is_single_use(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Rotate Test", "email": "rotate.test@example.com", "password": "correct-horse-battery"},
    )
    old_refresh_cookie = client.cookies.get("refresh_token")

    first_refresh = client.post("/api/v1/auth/refresh")
    assert first_refresh.status_code == 200

    # Manually replay the OLD refresh token (simulating a stolen, already-used token)
    client.cookies.set("refresh_token", old_refresh_cookie)
    replayed = client.post("/api/v1/auth/refresh")
    assert replayed.status_code == 401


def test_logout_revokes_refresh_token(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Logout Test", "email": "logout.test@example.com", "password": "correct-horse-battery"},
    )
    logout_response = client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 204

    # The refresh token that was valid a moment ago should now be rejected
    refresh_after_logout = client.post("/api/v1/auth/refresh")
    assert refresh_after_logout.status_code == 401
