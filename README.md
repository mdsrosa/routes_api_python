# Routes API
###### Python version of http://github.com/mdsrosa/routes_api

[![Build Status](https://travis-ci.org/mdsrosa/routes_api_python.svg)](https://travis-ci.org/mdsrosa/routes_api_python) [![Coverage Status](https://coveralls.io/repos/mdsrosa/routes_api_python/badge.svg?branch=master&service=github)](https://coveralls.io/github/mdsrosa/routes_api_python?branch=master)

API to calculate the shortest path and the cost to a given route (origin point and destination point), based on fuel price and vehicle's autonomy.

# Installation
###### **Considering you already have a Python development environment setup.**

```bash
$ git clone https://github.com/mdsrosa/routes_api_python.git
$ cd routes_api_python
$ mkvirtualenv routes-api-dev
$ pip install -r requirements.txt
```

### Running Locally
```bash
$ python db.py create
$ python run.py
```

# Endpoints

#### GET /routes

This endpoint lists all routes in the database.

#### cURL Example

```bash
$ curl -i http://localhost:5000/routes
```
#### Response Example
```bash
{
    "routes": [
        {
            "destination_point": "B",
            "distance": 10,
            "origin_point": "A",
            "uri": "/routes/1"
        },
        {
            "destination_point": "C",
            "distance": 20,
            "origin_point": "A",
            "uri": "/routes/2"
        },
        {
            "destination_point": "D",
            "distance": 15,
            "origin_point": "B",
            "uri": "/routes/3"
        },
        {
            "destination_point": "D",
            "distance": 30,
            "origin_point": "C",
            "uri": "/routes/4"
        },
        {
            "destination_point": "E",
            "distance": 50,
            "origin_point": "B",
            "uri": "/routes/5"
        },
        {
            "destination_point": "E",
            "distance": 30,
            "origin_point": "D",
            "uri": "/routes/6"
        }
    ]
}
```

#### GET `/routes/pk`
This endpoint returns a route.

##### cURL Example
```bash
$ curl -i http://localhost:5000/routes/1
```

##### Response Example
```bash
{
    "route": {
        "destination_point": "B",
        "distance": 10,
        "origin_point": "A",
        "uri": "/routes/1"
    }
}
```

#### POST `/routes`
This endpoint creates a new route.

#### Fields

Name            | Type | Description | Example
----------------|------|------------ |--------
**origin_point**| _string_ | The point of origin| `"A"`
**destination_point**| _string_ | The point of destination| `"D"`
**distance**| _integer_ |The vehicle's autonomy| `10`

##### cURL Example
```bash
$ curl -i -X POST -H "Content-Type: application/json" http://localhost:5000/routes -d '{"origin_point": "A", "destination_point": "D", "distance": 10}'
```

##### Response Example
```bash
{
    "route": {
        "destination_point": "D",
        "distance": 10,
        "origin_point": "A",
        "uri": "/routes/1"
    }
}
```

#### PUT `/routes/pk`
This endpoint updates a route.

#### Fields

Name            | Type | Description | Example
----------------|------|------------ |--------
**origin_point**| _string_ | The point of origin| `"A"`
**destination_point**| _string_ | The point of destination| `"D"`
**distance**| _integer_ |The vehicle's autonomy| `10`

##### cURL Example
```bash
$ curl -i -X PUT -H "Content-Type: application/json" http://localhost:5000/routes/1 -d '{"destination_point": "B"}'
```

##### Response Example
```bash
{
    "route": {
        "destination_point": "B",
        "distance": 10,
        "origin_point": "A",
        "uri": "/routes/1"
    }
}
```

#### DELETE `/routes/pk`
This endpoint deletes a route.

##### cURL Example
```bash
$ curl -X DELETE http://localhost:5000/routes/1
```

##### Response Example
```bash
{
    "result": true
}
```

#### POST `/routes/calculate-cost`

This endpoint calculates the cost based on `distance`,  `autonomy` and `fuel_price`.

#### Fields

Name            | Type | Description | Example
----------------|------|------------ |--------
**origin_point**| _string_ | The point of origin| `"A"`
**destination_point**| _string_ | The point of destination| `"D"`
**autonomy**| _integer_ |The vehicle's autonomy| `10`
**fuel_price**| _float_ |The fuel price|`2.5`

##### cURL Example
```bash
$ curl -i -H "Content-Type: application/json" http://localhost:5000/routes/calculate-cost -d '{"origin_point":"A","destination_point": "D","autonomy":10,"fuel_price":2.5}'
```
##### Response Example
```json
{
    "cost": 6.25,
    "path": "A B D"
}
```

# Testing
```bash
python tests.py
```