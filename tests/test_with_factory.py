from .factories import ClientFactory, ParkingFactory
from ..flask_app.models import Client, Parking

def test_create_client(app, db):
    client_new = ClientFactory()
    db.session.commit()
    assert client_new.id is not None
    assert len(db.session.query(Client).all()) == 2

def test_create_parking(app, db):
    parking_new = ParkingFactory()
    db.session.commit()
    assert parking_new.id is not None
    assert len(db.session.query(Parking).all()) == 2

