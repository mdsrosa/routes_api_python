from app import db
from app.dijkstra import Graph, get_shortest_path
from flask.ext.sqlalchemy import sqlalchemy


class Base(db.Model):

    __abstract__ = True

    pk = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Route(Base):

    __tablename__ = 'routes'

    origin_point = db.Column(db.String(128), nullable=False)
    destination_point = db.Column(db.String(128), nullable=False, )
    distance = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        sqlalchemy.UniqueConstraint('origin_point', 'destination_point', 'distance'),
    )

    def __repr__(self):
        return '<Route <{0}-{1}-{2}>'.format(self.origin_point,
                                             self.destination_point,
                                             self.distance)

    @classmethod
    def calculate(cls, origin, destination, autonomy, fuel_price):
        distance, path = cls._calculate_shortest_path(origin, destination)
        cost = cls._calculate_cost(distance, autonomy, fuel_price)

        return cost, ' '.join(path)

    def _calculate_shortest_path(origin, destination):
        graph = Graph()
        routes = Route.query.all()

        for route in routes:
            graph.add_node(route.origin_point)

        for route in routes:
            graph.add_edge(route.origin_point,
                           route.destination_point,
                           route.distance)

        return get_shortest_path(graph, origin, destination)

    def _calculate_cost(distance, autonomy, fuel_price):
        return distance * fuel_price / autonomy
