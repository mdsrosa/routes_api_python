from flask import abort
from flask.ext.restful import Resource, reqparse, marshal, fields
from app.models import Route


route_fields = {
    'uri': fields.Url('route'),
    'origin_point': fields.String,
    'destination_point': fields.String,
    'distance': fields.Integer
}


class RouteListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('origin_point', type=str, required=True,
                                   help='No origin_point provided',
                                   location='json')
        self.reqparse.add_argument('destination_point', type=str,
                                   required=True, help='No destination_point provided', location='json')
        self.reqparse.add_argument('distance', type=int, required=True,
                                   help='No distance provided',
                                   location='json')

        super(RouteListAPI, self).__init__()

    def get(self):
        routes = Route.query.all()
        return {'routes': [marshal(route, route_fields) for route in routes]}


class RouteAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('origin_point', type=str, location='json')
        self.reqparse.add_argument('destination_point', type=str,
                                   location='json')
        self.reqparse.add_argument('distance', type=int, location='json')

        super(RouteAPI, self).__init__()

    def get(self, pk):
        route = Route.query.get(pk)
        if not route:
            abort(404)
        return {'route': marshal(route, route_fields)}
