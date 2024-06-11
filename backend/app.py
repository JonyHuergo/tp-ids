from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///test.db?charset=utf8mb4')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cabins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.Text)

class Habitaciones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabin_id = db.Column(db.Integer, db.ForeignKey('cabins.id'))
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10,2))
    imagen = db.Column(db.Text)

class Reservas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabin_id = db.Column(db.Integer, db.ForeignKey('cabins.id'))
    nombre = db.Column(db.String(255), nullable=False)
    cantidad_personas = db.Column(db.Integer)
    fecha_ingreso = db.Column(db.Date)
    fecha_salida = db.Column(db.Date)

@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/cabins')
def get_all_cabins():
    cabins = Cabins.query.all()

    results = []
    for cabin in cabins:
        result = {
            'id': cabin.id,
            'nombre': cabin.nombre,
            'descripcion': cabin.descripcion,
            'imagen': cabin.imagen
        }
        results.append(result)

    return jsonify(results)

@app.route('/cabins/<int:id>')
def get_cabin(id):
    cabin = Cabins.query.get(id)

    if cabin is None:
        return jsonify({'error': 'La cabaña no se ha encontrado'}), 404

    result = {
        'id': cabin.id,
        'nombre': cabin.nombre,
        'descripcion': cabin.descripcion,
        'imagen': cabin.imagen
    }

    return jsonify(result)

@app.route('/habitaciones')
def get_rooms():
    cabin_id = request.args.get('cabin_id', default=None, type=int)
    min_precio = request.args.get('min_precio', default=None, type=float)
    max_precio = request.args.get('max_precio', default=None, type=float)

    query = Habitaciones.query

    if cabin_id is not None:
        query = query.filter(Habitaciones.cabin_id == cabin_id)

    if min_precio is not None:
        query = query.filter(Habitaciones.precio >= min_precio)

    if max_precio is not None:
        query = query.filter(Habitaciones.precio <= max_precio)

    habitaciones = query.all()

    results = []
    for habitacion in habitaciones:
        result = {
            'id': habitacion.id,
            'cabin_id': habitacion.cabin_id,
            'nombre': habitacion.nombre,
            'descripcion': habitacion.descripcion,
            'precio': str(habitacion.precio),
            'imagen': habitacion.imagen
        }
        results.append(result)

    return jsonify(results)

@app.route('/habitaciones/<int:id>')
def get_room(id):
    habitacion = Habitaciones.query.get(id)

    if habitacion is None:
        return jsonify({'error': 'La habitacion no se ha encontrado'}), 404

    result = {
        'id': habitacion.id,
        'cabin_id': habitacion.cabin_id,
        'nombre': habitacion.nombre,
        'descripcion': habitacion.descripcion,
        'precio': str(habitacion.precio),
        'imagen': habitacion.imagen
    }

    return jsonify(result)

@app.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()
    reserva = Reservas(cabin_id=data['cabin_id'], nombre=data['nombre'], cantidad_personas=data['cantidad_personas'], fecha_ingreso=data['fecha_ingreso'], fecha_salida=data['fecha_salida'])
    db.session.add(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva created'}), 201

@app.route('/reservas/<int:id>', methods=['GET'])
def get_reserva(id):
    reserva = Reservas.query.get(id)
    if reserva is None:
        return jsonify({'error': 'Reserva not found'}), 404
    return jsonify({'id': reserva.id, 'cabin_id': reserva.cabin_id, 'nombre': reserva.nombre, 'cantidad_personas': reserva.cantidad_personas, 'fecha_ingreso': str(reserva.fecha_ingreso), 'fecha_salida': str(reserva.fecha_salida)})

@app.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    data = request.get_json()
    reserva = Reservas.query.get(id)
    if reserva is None:
        return jsonify({'error': 'Reserva not found'}), 404
    reserva.cabin_id = data['cabin_id']
    reserva.nombre = data['nombre']
    reserva.cantidad_personas = data['cantidad_personas']
    reserva.fecha_ingreso = data['fecha_ingreso']
    reserva.fecha_salida = data['fecha_salida']
    db.session.commit()
    return jsonify({'message': 'Reserva updated'})

@app.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reservas.query.get(id)
    if reserva is None:
        return jsonify({'error': 'Reserva not found'}), 404
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
