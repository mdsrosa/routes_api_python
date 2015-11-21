from app import db


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Route(Base):

    __tablename__ = 'routes'

    origin_point = db.Column(db.String(128), nullable=False)
    destination_point = db.Column(db.String(128), nullable=False)
    distance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Route <{0}-{1}-{2]>'.format(self.origin_pint,
                                             self.destination_point,
                                             self.distance)
