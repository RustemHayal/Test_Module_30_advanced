import factory, random

from ..flask_app.app import db
from ..flask_app.models import Client, Client_Parking, Parking

def number_of_car():
    number_list = str
    for num in range(1, 6):
        if num == [1,5,6]:
            number_list = number_list + random.choice('АВЕКМНОРСТУХ')
        else:
            numer=random.randint(0, 9)
            number_list=f"{number_list}{str(numer)}"
    return number_list

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyAttribute(lambda x: random.randint(1000000000000000, 9999999999999999))
    car_number =  number_of_car()

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    opened = True
    count_places = factory.LazyAttribute(lambda x:random.randint(10, 150)) # в среднем на парковках города от 10 до 150 мест
    count_available_places = count_places #одно парковочное место для нужд администрации

