from common.schema.booking_schema import get_booking_schema
from common.utils import is_validate


class TestGetBooking:
    def test_get_booking(self, auth_client, create_booking):
        """
           1. Add new booking
           2. Get created booking by id
           3. Check data and status
           4. Validate schema
        """
        id_booking = create_booking.get("bookingid")
        res = auth_client.get_booking(id_booking)
        assert res.json() == create_booking.get("booking")
        assert is_validate(res.json(), get_booking_schema), "Check booking schema"
