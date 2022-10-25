"""
    Routes API Tests
    ~~~~~~~~~~~~~~~~

    Tests for the Routes API
"""

import json
import unittest

from app import app, db
from app.models import Route


def clean_db(func):
    def inner(*args, **kwargs):
        with app.app_context():
            db.drop_all()
            db.create_all()
            return func(*args, **kwargs)

    return inner


class RouteModelTestCase(unittest.TestCase):
    def setUp(self):
        self.route = Route(origin_point="A", destination_point="B", distance=10)

    def test_route_representation(self):
        route = self.route
        expected = "<Route A-B-10>"

        self.assertEqual(expected, repr(route))


class RouteApiTestCase(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.config["TESTING"] = True
            app.config[
                "SQL_ALCHEMY_DATABASE_URI"
            ] = "postgresql://localhost/routes_api_python_test"
            self.app = app.test_client()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_endpoint(self):
        response = self.app.get("/")
        expected = "Routes API Python Version :)"
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected, result)

    def test_nonexistent_endpoint(self):
        response = self.app.get("/nonexistent")
        expected = "Not found"
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 404)
        self.assertIn(expected, result)


class RoutesApiTestCase(RouteApiTestCase):
    def test_empty_database(self):
        response = self.app.get("/routes")
        expected = '{\n"routes":[]\n}\n'
        result = response.data.decode("utf-8").replace(" ", "")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    @clean_db
    def test_show_all_routes(self):
        route = Route(origin_point="A", destination_point="B", distance=10)
        db.session.add(route)
        db.session.commit()
        expected = {
            "routes": [
                {
                    "destination_point": "B",
                    "distance": 10,
                    "origin_point": "A",
                    "uri": "/routes/1",
                }
            ]
        }

        response = self.app.get("/routes")
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    @clean_db
    def test_create_route(self):
        route = {"origin_point": "A", "destination_point": "C", "distance": 20}
        data = json.dumps(route)
        expected = {
            "route": {
                "origin_point": "A",
                "destination_point": "C",
                "distance": 20,
                "uri": "/routes/1",
            }
        }

        response = self.app.post("/routes", data=data, content_type="application/json")
        result = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result, expected)

    @clean_db
    def test_create_route_uniqueness(self):
        route = {"origin_point": "A", "destination_point": "C", "distance": 20}
        data = json.dumps(route)

        # first post
        response = self.app.post("/routes", data=data, content_type="application/json")
        expected = {
            "route": {
                "destination_point": "C",
                "distance": 20,
                "origin_point": "A",
                "uri": "/routes/1",
            }
        }
        result = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result, expected)

        # second post
        response = self.app.post("/routes", data=data, content_type="application/json")
        expected = "Route already exists."
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 400)
        self.assertIn(expected, result)

    @clean_db
    def test_create_route_with_invalid_data(self):
        route = {"origin_point": "A", "destination_point": "B", "distance": "ABC"}

        data = json.dumps(route)

        response = self.app.post("/routes", data=data, content_type="application/json")
        expected = "Value 'ABC' for field 'distance' is not a valid integer."
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 400)
        self.assertIn(expected, result)

    @clean_db
    def test_update_route_destination_point(self):
        route = Route(origin_point="A", destination_point="C", distance=10)
        db.session.add(route)
        db.session.commit()

        fields_to_update = {"destination_point": "B"}
        data = json.dumps(fields_to_update)
        response = self.app.put(
            "/routes/{}".format(route.pk), data=data, content_type="application/json"
        )
        expected = {
            "route": {
                "destination_point": "B",
                "distance": 10,
                "origin_point": "A",
                "uri": "/routes/1",
            }
        }
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    @clean_db
    def test_update_route_origin_point(self):
        route = Route(origin_point="A", destination_point="C", distance=10)
        db.session.add(route)
        db.session.commit()

        fields_to_update = {"origin_point": "B"}

        data = json.dumps(fields_to_update)

        response = self.app.put(
            "/routes/{}".format(route.pk), data=data, content_type="application/json"
        )
        expected = {
            "route": {
                "destination_point": "C",
                "distance": 10,
                "origin_point": "B",
                "uri": "/routes/1",
            }
        }
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    @clean_db
    def test_update_route_distance(self):
        route = Route(origin_point="A", destination_point="C", distance=10)
        db.session.add(route)
        db.session.commit()

        fields_to_update = {"distance": 20}
        data = json.dumps(fields_to_update)

        response = self.app.put(
            "/routes/{}".format(route.pk), data=data, content_type="application/json"
        )
        expected = {
            "route": {
                "destination_point": "C",
                "distance": 20,
                "origin_point": "A",
                "uri": "/routes/1",
            }
        }
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    def test_update_nonexistent_route(self):
        fields_to_update = {"destination_point": "B"}
        data = json.dumps(fields_to_update)
        response = self.app.put(
            "/routes/123", data=data, content_type="application/json"
        )
        expected = "Route not found"
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 404)
        self.assertIn(expected, result)

    @clean_db
    def test_get_route(self):
        route = Route(origin_point="A", destination_point="B", distance=10)
        db.session.add(route)
        db.session.commit()

        response = self.app.get("/routes/{}".format(route.pk))
        expected = {
            "route": {
                "destination_point": "B",
                "distance": 10,
                "origin_point": "A",
                "uri": "/routes/1",
            }
        }
        result = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    def test_get_nonexistent_route(self):
        response = self.app.get("/routes/123")
        expected = "Route not found"
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 404)
        self.assertIn(expected, result)

    @clean_db
    def test_delete_route(self):
        route = Route(origin_point="A", destination_point="B", distance=10)
        db.session.add(route)
        db.session.commit()

        response = self.app.delete("/routes/{}".format(route.pk))
        expected = '{\n"result":true\n}\n'
        result = response.data.decode("utf-8").replace(" ", "")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    def test_delete_nonexistent_route(self):
        response = self.app.delete("/routes/1234")
        expected = "Route not found"
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 404)
        self.assertIn(expected, result)


class RouteCalculateCostApiTestCase(RouteApiTestCase):
    def setUp(self):
        with app.app_context():
            app.config["TESTING"] = True
            app.config[
                "SQL_ALCHEMY_DATABASE_URI"
            ] = "postgresql://localhost/routes_api_python_test"
            self.app = app.test_client()
            db.create_all()

            # routes
            self._create_routes()

    def _create_routes(self):
        # routes
        routes = [
            Route(origin_point="A", destination_point="B", distance=10),
            Route(origin_point="A", destination_point="C", distance=20),
            Route(origin_point="B", destination_point="D", distance=15),
            Route(origin_point="C", destination_point="D", distance=30),
            Route(origin_point="B", destination_point="E", distance=50),
            Route(origin_point="D", destination_point="E", distance=30),
        ]

        for route in routes:
            db.session.add(route)

        db.session.commit()

    def test_calculate_cost(self):
        data = {
            "origin_point": "A",
            "destination_point": "D",
            "autonomy": 10,
            "fuel_price": 2.5,
        }

        data = json.dumps(data)

        response = self.app.post(
            "/routes/calculate-cost", data=data, content_type="application/json"
        )

        expected = '{\n"cost":6.25,\n"path":"ABD"\n}\n'
        result = response.data.decode("utf-8").replace(" ", "")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    def test_calculate_cost_with_invalid_data(self):
        data = {
            "origin_point": "A",
            "destination_point": "D",
            "autonomy": "ABC",
            "fuel_price": 2.5,
        }

        data = json.dumps(data)

        response = self.app.post(
            "/routes/calculate-cost", data=data, content_type="application/json"
        )
        expected = "Value 'ABC' for field 'autonomy' is not a valid integer."
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 400)
        self.assertIn(expected, result)

    def test_calculate_cost_with_invalid_fuel_price_data(self):
        data = {
            "origin_point": "A",
            "destination_point": "D",
            "autonomy": 10,
            "fuel_price": "XYZ",
        }

        data = json.dumps(data)

        response = self.app.post(
            "/routes/calculate-cost", data=data, content_type="application/json"
        )
        expected = "Value 'XYZ' for field 'fuel_price' is not a valid float."
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 400)
        self.assertIn(expected, result)

    def test_calculate_cost_with_missing_fields(self):
        data = {"origin_point": "A", "autonomy": 10, "fuel_price": 2.5}

        data = json.dumps(data)

        response = self.app.post(
            "/routes/calculate-cost", data=data, content_type="application/json"
        )
        expected = "Missing required parameter in the JSON body"
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 400)
        self.assertIn("destination_point", result)
        self.assertIn(expected, result)

    def test_calculate_cost_with_nonexistent_origin_point(self):
        data = {
            "origin_point": "Y",
            "destination_point": "A",
            "autonomy": 10,
            "fuel_price": 2.5,
        }

        data = json.dumps(data)

        response = self.app.post(
            "/routes/calculate-cost", data=data, content_type="application/json"
        )
        expected = "Origin point 'Y' not found"
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 400)
        self.assertIn(expected, result)

    def test_calculate_cost_with_nonexistent_destination_point(self):
        data = {
            "origin_point": "A",
            "destination_point": "X",
            "autonomy": 10,
            "fuel_price": 2.5,
        }

        data = json.dumps(data)

        response = self.app.post(
            "/routes/calculate-cost", data=data, content_type="application/json"
        )
        expected = "Destination point 'X' not found"
        result = response.data.decode("utf-8")

        self.assertEqual(response.status_code, 400)
        self.assertIn(expected, result)


if __name__ == "__main__":
    unittest.main()
