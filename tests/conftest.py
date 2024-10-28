import pytest
from datetime import datetime

from module_29_testing.hw.flask_app.app import create_app, db as _db
from module_29_testing.hw.flask_app.models import Client, Client_Parking, Parking

@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client = Client(
            name="Иван",
            surname="Иванов",
            credit_card="1234123412341234",
            car_number="В000ВВ"
        )
        parking = Parking(
            address="Первое мая д.1",
            opened=True,
            count_places=10,
            count_available_places=5
        )
        client_parking=Client_Parking(
            client_id=1,
            parking_id=1,
            time_in=datetime.strptime('2024-10-24 12:06:09', "%Y-%m-%d %H:%M:%S"),
            time_out=datetime.strptime('2024-10-24 13:10:19', "%Y-%m-%d %H:%M:%S")
        )
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()

@pytest.fixture
def client(app):
    client = app.test_client()
    yield client

@pytest.fixture
def parking(app):
    parking = app.test_client()
    yield parking

@pytest.fixture
def client_parking(app):
    client_parking=app.test_client()
    yield client_parking

@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
