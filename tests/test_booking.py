import pytest

from common.schema.booking_schema import post_booking_schema
from common.utils import is_validate
from model.booking import BookingData


class TestCreateBooking:
    def test_create_new_booking(self, auth_client):
        data = BookingData().random()
        res = auth_client.create_booking(data)
        assert res.status_code == 200
        booking_info = res.json()
        assert booking_info.get("booking") == data.object_to_dict()
        assert is_validate(booking_info, post_booking_schema), "Check booking schema"

    def test_create_new_booking_unauth_client(self, unauth_client):
        data = BookingData().random()
        res = unauth_client.create_booking(data)
        assert res.status_code == 200
        booking_info = res.json()
        assert booking_info.get("booking") == data.object_to_dict()

    @pytest.mark.parametrize(
        "attr", ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
    )
    def test_create_booking_with_empty_requiered_field(self, auth_client, attr):
        data = BookingData().random()
        setattr(data, attr, None)
        res = auth_client.create_booking(data)
        assert res.status_code == 500

    @pytest.mark.parametrize("attr", ["checkin", "checkout"])
    def test_create_booking_with_empty_bookingdates_fields(self, auth_client, attr):
        data = BookingData().random()
        setattr(data.bookingdates, attr, None)
        res = auth_client.create_booking(data)
        assert res.status_code == 500

    def test_create_booking_with_empty_optional_field(self, auth_client):
        data = BookingData().random()
        setattr(data, "additionalneeds", None)
        res = auth_client.create_booking(data)
        assert res.status_code == 200
        booking_info = res.json()
        assert booking_info.get("booking") == data.object_to_dict()

    @pytest.mark.parametrize(
        "attr", ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
    )
    def test_create_booking_without_one_required_field(self, auth_client, attr):
        data = BookingData().random()
        delattr(data, attr)
        res = auth_client.create_booking(data)
        assert res.status_code == 500

    def test_create_booking_without_one_optional_field(self, auth_client):
        data = BookingData().random()
        delattr(data, "additionalneeds")
        res = auth_client.create_booking(data)
        assert res.status_code == 200
        booking_info = res.json()
        assert booking_info.get("booking") == data.object_to_dict()

    @pytest.mark.parametrize(
        "attr, incorrect_type",
        [
            ("firstname", int),
            ("lastname", int),
            pytest.param(
                "totalprice", str, marks=pytest.mark.xfail(reason="no type validation")
            ),
            pytest.param(
                "depositpaid", str, marks=pytest.mark.xfail(reason="no type validation")
            ),
            ("bookingdates", bool),
        ],
    )
    def test_create_booking_incorrect_param_type(
        self, auth_client, attr, incorrect_type
    ):
        data = BookingData().random()
        setattr(data, attr, incorrect_type(1))
        res = auth_client.create_booking(data)
        assert res.status_code == 500

    def test_new_booking_empty_data(self, auth_client):
        data = BookingData()
        res = auth_client.create_booking(data)
        assert res.status_code == 500
