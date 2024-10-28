from typing import List
from xmlrpc.client import boolean

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
    db.init_app(app)

    from .models import Client, Parking, Client_Parking
    @app.before_request
    def before_request_app():
        app.before_request_funcs[None].remove(before_request_app)
        db.create_all()
        return "Добро пожаловать" , "100"

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route('/clients', methods=['GET'])
    def get_client_handlers():
        """Вывод всех пользователей в формате json"""
        clients: List[Client] = db.session.query(Client).all()
        client_list = [client.to_json() for client in clients]
        return jsonify(client_list), 200

    @app.route('/clients', methods=['POST'])
    def add_new_client():
        """Создание нового клиента.
        Пример запроса: http post http://127.0.0.1:5000/clients name='Иван' surname='Иванов' credit_card=1111111111111111 car_number='A 000 AA'
        """
        new_client_add = request.json
        new_client = Client(
            name=new_client_add['name'],
            surname=new_client_add['surname'],
            credit_card=int(new_client_add['credit_card']),
            car_number=new_client_add['car_number']
        )
        db.session.add(new_client)
        data = new_client.to_json()
        db.session.commit()
        return f"{data}", 201

    @app.route('/clients/<int:client_id>', methods=["GET"])
    def get_client_id_handler(client_id):
        """Вывод информации про клиента по id номеру
        Пример запроса: http http://127.0.0.1:5000/clients/1
        """
        client = db.session.query(Client).filter(Client.id==client_id).one()
        return jsonify(client.to_json()), 200

    @app.route('/parking', methods=['POST'])
    def add_new_parking():
        """Создание новой парковочной зоны.
        Пример запроса: http post http://127.0.0.1:5000/parking address='Ленина, д. 15' opened=1 count_places=100 count_available_places=100
        """
        new_parking_add=request.json
        new_parking=Parking(
            address=new_parking_add['address'],
            opened=bool(new_parking_add['opened']),
            count_places=int(new_parking_add['count_places']),
            count_available_places=int(new_parking_add['count_available_places'])
        )
        db.session.add(new_parking)
        data = new_parking.to_json()
        db.session.commit()
        return f'{data}', 200

    @app.route('/client_parking', methods=['POST'])
    def add_client_parking():
        """
        Оформление при заезде на парковку. При заезде камера считывает гос. номера, по которым определяется id номер клиента.
        Номер id парковки заранее известен.
        Для проверки:
        http post http://127.0.0.1:5000/client_parking client_id=1 parking_id=1
        """
        client_parking_going=request.json
        parking=db.session.query(Parking).filter(Parking.id==client_parking_going['parking_id']).one()

        if parking.opened == True:

            new_client_parking_post=Client_Parking(
                client_id=client_parking_going['client_id'],
                parking_id=client_parking_going['parking_id'],
                time_in=datetime.now()
            )
            parking.count_available_places -= 1
            if parking.count_available_places <= 0:
                parking.opened=False
            db.session.add(new_client_parking_post)
            db.session.commit()
            return "Проезжайте"

        else:
            return "Свободных мест нет, подождите пока выедет машина."

    @app.route('/client_parking', methods=["DELETE"])
    def delete_client_parking():
        """
        Оформление при выезде автомашины.
        Пример запроса: http delete http://127.0.0.1:5000/client_parking client_id=1 parking_id=1
        """
        client_parking_go=request.json
        client_parking = db.session.query(Client_Parking).filter(Client_Parking.client_id==client_parking_go['client_id']).one()
        client=db.session.query(Client).filter(Client.id==client_parking_go['client_id']).one()
        if client.credit_card:
            client_parking.time_out=datetime.now()
            timer_parking= format(client_parking.time_out - client_parking.time_in, "%H:%M")
            return f"Денежные средства за парковку {timer_parking}ч:мин будут списаны с Вашей карты"
        else:
            return "Привяжите действующую карту к нашему приложению, пока Вы это не сделаете, мы не можем Вас выпустить"

    return app
  
