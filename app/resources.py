from flask import abort
from flask.ext.restful import Resource, reqparse, marshal, fields
from flask.ext.sqlalchemy import sqlalchemy
from app.models import Route
from app.fields import integer_field, float_field
from app import db


route_fields = {
    'origin_point': fields.String,
    'destination_point': fields.String,
    'distance': fields.Integer,
    'uri': fields.Url('route'),
}


class RoutesAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('origin_point', type=str, required=True,
                                   location='json')
        self.reqparse.add_argument('destination_point', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('distance', type=integer_field,
                                   required=True, location='json')

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

        try:
            route_object = Route(**route)
            db.session.add(route_object)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return {'error': 'Route already exists.'}, 400

        return {'route': marshal(route_object, route_fields)}, 201


class RouteAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('origin_point', type=str, location='json')
        self.reqparse.add_argument('destination_point', type=str,
                                   location='json')
        self.reqparse.add_argument('distance', type=integer_field, location='json')

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


class RouteCalculateCostAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('origin_point', type=str, required=True,
                                   location='json')
        self.reqparse.add_argument('destination_point', type=str,
                                   required=True, location='json')
        self.reqparse.add_argument('autonomy', type=integer_field, required=True,
                                   location='json')
        self.reqparse.add_argument('fuel_price', type=float_field,
                                   required=True, location='json')

        super(RouteCalculateCostAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        origin_point = args.get('origin_point')
        destination_point = args.get('destination_point')
        autonomy = args.get('autonomy')
        fuel_price = args.get('fuel_price')

        # validate origin point and destination point
        if Route.query.filter_by(origin_point=origin_point).count() == 0:
            return {'error': 'Origin point "%s" not found' % origin_point}, 400

        if Route.query.filter_by(destination_point=destination_point).count() == 0:
            return {'error': 'Destination point "%s" not found' % destination_point}, 400

        cost, path = Route.calculate(origin_point, destination_point,
                                     autonomy, fuel_price)
        return {'cost': cost, 'path': path}
