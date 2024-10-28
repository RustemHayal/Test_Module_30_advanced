import pytest
from datetime import datetime

from module_29_testing.hw.test.conftest import parking


def test_create_client(client):
    client_data = {'name':"Иван", 'surname':"Иванов", 'credit_card':"1234123412341234", 'car_number':"В000ВВ"}
    result = client.post('/clients', data=client_data)
    assert result.status_code==200

def test_create_parking(parking):
    parking_data = {'address':"Первое мая д.1", "opened":bool('True'), 'count_places':int('10'), 'count_available_places':int('5')}
    result = parking.post('/parking', data=parking_data)
    assert result.status_code==200

def client_check_in_parking(parking):
    if parking.opened == True:
        return {'client_id':1, 'parking_id':1, 'time_in':datetime.strptime('2024-10-24 10:15', '%Y-%m-%d %H:%M')}
    else:
        return "NOT PLACES"

def client_chek_out_parking(client):
    if client.card_credits:
        return '2024-10-24 12:15'
    else:
        return "Your not card_credits"

@pytest.mark.parametrize("route", '/client_parking')
def test_client_going_parking(client_parking, route):
    parking = {'address': "Первое мая д.1", "opened": bool('True'), 'count_places': int('10'),
               'count_available_places': int('5')}
    client_data = {'name': "Иван", 'surname': "Иванов", 'credit_card': "1234123412341234", 'car_number': "В000ВВ"}
    if route == 'POST':
        data = client_parking.post({'client_id':1, 'parking_id':1, 'time_in':datetime.strptime('2024-10-24 10:15', '%Y-%m-%d %H:%M')})
        res_data = client_check_in_parking(parking)
        assert data == res_data
    elif route == 'DELETE':
        data_time_out = client_chek_out_parking(client_data)
        parking['time_out'] = datetime.strptime(data_time_out, '%Y-%m-%d %H:%M')
        assert parking['time_out'] == datetime.strptime('2024-10-24 12:15', '%Y-%m-%d %H:%M')

@pytest.mark.parametrize("route", ['/clients', '/clients/1'])
def test_route_status(client, route):
    data=client.get(route)
    assert data.status_code==200
