"""
    Routes API Tests
    ~~~~~~~~~~~~~~~~

    Tests for the Routes API
"""

import os
import json
import unittest

from config import BASE_DIR
from app import app, db
from app.models import Route


def clean_db(func):
    def inner(*args, **kwargs):
        db.drop_all()
        db.create_all()
        return func(*args, **kwargs)
    return inner


class RoutesApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_database(self):
        response = self.app.get('/routes')
        expected = b'{\n    "routes": []\n}\n'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

    @clean_db
    def test_show_all_routes(self):
        route = Route(origin_point="A", destination_point="B", distance=10)
        db.session.add(route)
        db.session.commit()
        expected = b'{\n    "routes": [\n        {\n            "destination_point": "B",\n            "distance": 10,\n            "origin_point": "A",\n            "uri": "/routes/1"\n        }\n    ]\n}\n'

        response = self.app.get('/routes')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

    @clean_db
    def test_create_route(self):
        route = {
            "origin_point": "A",
            "destination_point": "C",
            "distance": 20
        }
        data = json.dumps(route)
        expected = b'{\n    "route": {\n        "destination_point": "C",\n        "distance": 20,\n        "origin_point": "A",\n        "uri": "/routes/1"\n    }\n}\n'

        response = self.app.post('/routes', data=data, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected)

    @clean_db
    def test_create_route_uniqueness(self):
        route = {
            "origin_point": "A",
            "destination_point": "C",
            "distance": 20
        }

        data = json.dumps(route)

        # first post
        response = self.app.post('/routes', data=data, content_type="application/json")
        expected = b'{\n    "route": {\n        "destination_point": "C",\n        "distance": 20,\n        "origin_point": "A",\n        "uri": "/routes/1"\n    }\n}\n'

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected)

        # second post
        response = self.app.post('/routes', data=data, content_type="application/json")
        expected = b'{\n    "error": "Route already exists."\n}\n'

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected)

    @clean_db
    def test_create_route_with_invalid_data(self):
        route = {
            "origin_point": "A",
            "destination_point": "B",
            "distance": "ABC"
        }

        data = json.dumps(route)

        response = self.app.post('/routes', data=data, content_type="application/json")
        expected = b'{\n    "message": {\n        "distance": "Value \'ABC\' for field \'distance\' is not a valid integer."\n    }\n}\n'

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected)

    @clean_db
    def test_update_route(self):
        route = Route(origin_point="A", destination_point="C", distance=10)
        db.session.add(route)
        db.session.commit()

        fields_to_update = {
            "destination_point": "B"
        }

        data = json.dumps(fields_to_update)

        response = self.app.put('/routes/{}'.format(route.pk),
                                data=data, content_type="application/json")
        expected = b'{\n    "route": {\n        "destination_point": "B",\n        "distance": 10,\n        "origin_point": "A",\n        "uri": "/routes/1"\n    }\n}\n'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

    @clean_db
    def test_get_route(self):
        route = Route(origin_point="A", destination_point="B", distance=10)
        db.session.add(route)
        db.session.commit()

        response = self.app.get('/routes/{}'.format(route.pk))
        expected = b'{\n    "route": {\n        "destination_point": "B",\n        "distance": 10,\n        "origin_point": "A",\n        "uri": "/routes/1"\n    }\n}\n'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

if __name__ == '__main__':
    unittest.main()
