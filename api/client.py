import requests

from model.booking import BookingData
from model.login_auth import UserData
from utilities.utils import logging as log


class Client:
    s = requests.Session()

    def __init__(self, url):
        self.url = url

    def auth(self, user_data: UserData):
        data = user_data.__dict__
        return self.s.post(self.url + "/auth", json=data)

    def set_cookies(self, user_data: UserData):
        res = self.auth(user_data)
        if res.status_code != 200:
            raise Exception("Error to authorize")
        session_token = res.json().get("token")
        cookie = requests.cookies.create_cookie("token", session_token)
        self.s.cookies.set_cookie(cookie)
        return res.json().get("token")

    @log("Get booking by id")
    def create_booking(self, data: BookingData):
        data = data.object_to_dict()
        return self.s.post(self.url + "/booking", json=data)
