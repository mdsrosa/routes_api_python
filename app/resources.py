from flask import abort
from flask.ext.restful import Resource, reqparse, marshal, fields
from app.models import Route
from app import db


route_fields = {
    'uri': fields.Url('route'),
    'origin_point': fields.String,
    'destination_point': fields.String,
    'distance': fields.Integer
}


class RoutesAPI(Resource):
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

        super(RoutesAPI, self).__init__()

    def get(self):
        routes = Route.query.all()
        return {'routes': [marshal(route, route_fields) for route in routes]}

    def post(self):
        args = self.reqparse.parse_args()
        route = {
            'origin_point': args.get('origin_point'),
            'destination_point': args.get('destination_point'),
            'distance': args.get('distance')
        }

        route_object = Route(**route)
        db.session.add(route_object)
        db.session.commit()

        return {'route': marshal(route_object, route_fields)}


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
        if route is None:
            abort(404)
        return {'route': marshal(route, route_fields)}

    def put(self, pk):
        route = Route.query.get(pk)
        if route is None:
            abort(404)

        args = self.reqparse.parse_args()

        if args.get('destination_point') is not None:
            route.destination_point = args.get('destination_point')

        if args.get('origin_point') is not None:
            route.origin_point = args.get('origin_point')

        if args.get('distance') is not None:
            route.distance = args.get('distance')

        db.session.commit()

        return {'route': marshal(Route.query.get(pk), route_fields)}

    def delete(self, pk):
        route = Route.query.get(pk)
        if route is None:
            abort(404)
        db.session.delete(route)
        db.session.commit()
        return {'result': True}