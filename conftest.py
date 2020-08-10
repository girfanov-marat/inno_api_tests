import logging

import pytest

from api.client import Client
from model.booking import BookingData
from model.login_auth import UserData
from common.logging import setup

logger = logging.getLogger()
setup()
logger.setLevel("INFO")


@pytest.fixture(scope="session")
def auth_client(request):
    url = request.config.getoption("--base-url")
    user = request.config.getoption("--username")
    password = request.config.getoption("--password")
    client = Client(url)
    user = UserData(user, password)
    client.set_cookies(user)
    return client


@pytest.fixture(scope="session")
def unauth_client(request):
    url = request.config.getoption("--base-url")
    client = Client(url)
    return client


@pytest.fixture()
def create_booking(auth_client):
    """
    Create new booking with random data
    :return: response dict
    """
    data = BookingData().random()
    res = auth_client.create_booking(data)
    return res.json()


@pytest.fixture()
def get_user(request):
    return request.config.getoption("--username")


@pytest.fixture()
def get_password(request):
    return request.config.getoption("--password")


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://restful-booker.herokuapp.com",
        help="enter base_url",
    ),
    parser.addoption(
        "--username", action="store", default="admin", help="enter username",
    ),
    parser.addoption(
        "--password", action="store", default="password123", help="enter password",
    ),
