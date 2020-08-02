from model.login_auth import UserData


def test_admin_login_empty_password(unauth_client, get_user):
    user = UserData(username=get_user, password=None)
    res = unauth_client.auth(user)
    data = res.json()
    assert data.get("reason") == "Bad credentials"
