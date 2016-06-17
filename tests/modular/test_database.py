# -*- coding:utf-8 -*-

import os.path
import unittest
import logging

from statik.models import *
from statik.database import *

GUEST_MODEL = """first-name: String
last-name: String
email: String
"""

GUESTHOUSE_MODEL = """guesthouse-name: String
address: Text
"""

GUESTHOUSE_ROOM_MODEL = """guesthouse: Guesthouse
room_name: String
"""

BOOKING_MODEL = """guest: Guest
room: GuesthouseRoom
from-date: DateTime
to-date: DateTime
"""

MOCK_MODEL_NAMES = ['Guest', 'Guesthouse', 'GuesthouseRoom', 'Booking']

MOCK_MODELS = {
    'Guest': StatikModel(name='Guest', from_string=GUEST_MODEL, model_names=MOCK_MODEL_NAMES),
    'Guesthouse': StatikModel(name='Guesthouse', from_string=GUESTHOUSE_MODEL, model_names=MOCK_MODEL_NAMES),
    'GuesthouseRoom': StatikModel(name='GuesthouseRoom', from_string=GUESTHOUSE_ROOM_MODEL, model_names=MOCK_MODEL_NAMES),
    'Booking': StatikModel(name='Booking', from_string=BOOKING_MODEL, model_names=MOCK_MODEL_NAMES),
}


class TestStatikDatabase(unittest.TestCase):

    """
    def setUp(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
        )
    """

    def test_database(self):
        data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_test_database')
        db = StatikDatabase(data_path, MOCK_MODELS)
        Guest = db.tables['Guest']
        Guesthouse = db.tables['Guesthouse']
        GuesthouseRoom = db.tables['GuesthouseRoom']
        Booking = db.tables['Booking']

        guests = db.session.query(Guest).order_by(Guest.last_name).all()
        self.assertEqual(2, len(guests))
        self.assertInstanceEqual({
            'first_name': 'Michael',
            'last_name': 'Anderson',
            'pk': 'manderson',
            'email': 'manderson@somewhere.com',
        }, guests[0])
        self.assertInstanceEqual({
            'first_name': 'Gary',
            'last_name': 'Merriweather',
            'pk': 'gmerriweather',
            'email': 'gmerriweather@somewhere.com',
        }, guests[1])

        guesthouses = db.session.query(Guesthouse).order_by(Guesthouse.guesthouse_name).all()
        self.assertEqual(2, len(guesthouses))
        self.assertInstanceEqual({
            'guesthouse_name': 'Firefly',
        }, guesthouses[0])
        self.assertInstanceEqual({
            'guesthouse_name': 'Red Cottage',
        }, guesthouses[1])

        guesthouse_rooms = db.session.query(GuesthouseRoom).order_by(GuesthouseRoom.room_name).all()
        self.assertEqual(2, len(guesthouse_rooms))
        self.assertInstanceEqual({
            'room_name': 'Blue Room',
            'guesthouse': guesthouses[1],
            'guesthouse_id': guesthouses[1].pk,
        }, guesthouse_rooms[0])
        self.assertInstanceEqual({
            'room_name': 'Red Room',
            'guesthouse': guesthouses[1],
            'guesthouse_id': guesthouses[1].pk,
        }, guesthouse_rooms[1])

        bookings = db.session.query(Booking).order_by(Booking.pk).all()
        self.assertEqual(2, len(bookings))
        self.assertInstanceEqual({
            'pk': '1',
            'guest': guests[1],
            'room': guesthouse_rooms[1],
        }, bookings[0])
        self.assertInstanceEqual({
            'pk': '2',
            'guest': guests[0],
            'room': guesthouse_rooms[0],
        }, bookings[1])

    def assertInstanceEqual(self, expected, inst):
        for field_name, field_value in expected.items():
            self.assertEqual(field_value, getattr(inst, field_name))


if __name__ == "__main__":
    unittest.main()