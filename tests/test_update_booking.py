from common.jsonpath import json_extractor
from common.schema.booking_schema import get_booking_schema
from common.utils import is_validate
from model.booking import BookingData


class TestUpdateBooking:
    def test_update_booking(self, auth_client, create_booking):
        """
           1. Add new booking
           2. Get created booking by id
           3. Update booking
        """
        data = BookingData().random()
        id_booking = create_booking.get("bookingid")
        res = auth_client.update_booking(id_booking, data)
        update_info = res.json()
        assert update_info == data.object_to_dict()
        assert is_validate(update_info, get_booking_schema), "Check booking schema"

    def test_update_booking_invalid_id(self, auth_client, non_exist_id=1000):
        """
           1. Add new booking
           2. Update booking with invalid id
        """
        data = BookingData().random()
        res = auth_client.update_booking(non_exist_id, data)
        assert res.status_code == 405

    def test_update_booking_invalid_id_new(self, auth_client):
        """
           1. Add new booking
           2. Get all booking ids
           3. Increase max id value by 10
           2. Update booking with non exist id
        """
        data = BookingData().random()
        get_bookings_res = auth_client.get_booking_ids()
        booking_ids = json_extractor(get_bookings_res.content, "$..bookingid")
        non_exist_id = max(booking_ids) + 10
        res = auth_client.update_booking(non_exist_id, data)
        assert res.status_code == 405
