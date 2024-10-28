from .app import db
from typing import Dict, Any
from sqlalchemy.ext.associationproxy import association_proxy

class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.Integer, nullable=False)
    car_number = db.Column(db.String(9), nullable=False)

    def __repr__(self):
        return f"Пользователь {self.name} {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

    client_parking=db.relationship("Client_Parking", back_populates='clients', cascade='all, delete-orphan')
    clients=association_proxy('client_parking', 'parking')

class Parking(db.Model):
    """
    address - адрес местонахождения парковки
    opened - открыта/закрыта в настоящее время
    count_places - количество мест в парковке
    count_available_places - количество доступных мест

    """
    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(150), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"Паркинг {self.address}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Client_Parking(db.Model):
    __tablename__='client_parking_s'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.ForeignKey('client.id'))
    parking_id = db.Column(db.ForeignKey('parking.id'))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    clients = db.relationship(Client, back_populates="client_parking")
    parking = db.relationship("Parking")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

