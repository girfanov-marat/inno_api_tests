from model.booking import BookingData


def test_create_new_booking(auth_client):
    data = BookingData().random()
    res = auth_client.create_booking(data)
    assert res.status_code == 200
    booking_info = res.json()
    assert booking_info.get("booking") == data.object_to_dict()
