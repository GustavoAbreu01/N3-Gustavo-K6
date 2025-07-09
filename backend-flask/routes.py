from flask import Blueprint, request, jsonify
from models import db, Dish

# Prefixo para API de pratos
bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')


@bp.route('/dishes', methods=['GET'])
def get_dishes():
    """Retorna lista de todos os pratos"""
    dishes = Dish.query.all()
    return jsonify([d.to_dict() for d in dishes]), 200


@bp.route('/dishes/<int:id>', methods=['GET'])
def get_dish(id):
    """Retorna um prato pelo ID"""
    dish = Dish.query.get_or_404(id)
    return jsonify(dish.to_dict()), 200


@bp.route('/dishes', methods=['POST'])
def create_dish():
    """Cria um novo prato"""
    data = request.get_json() or {}
    if not data.get('name') or data.get('price') is None:
        return jsonify({'error': 'Campos "name" e "price" são obrigatórios'}), 400
    dish = Dish(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price']
    )
    db.session.add(dish)
    db.session.commit()
    return jsonify(dish.to_dict()), 201


@bp.route('/dishes/<int:id>', methods=['PUT'])
def update_dish(id):
    """Atualiza um prato existente"""
    dish = Dish.query.get_or_404(id)
    data = request.get_json() or {}
    dish.name = data.get('name', dish.name)
    dish.description = data.get('description', dish.description)
    dish.price = data.get('price', dish.price)
    db.session.commit()
    return jsonify(dish.to_dict()), 200


@bp.route('/dishes/<int:id>', methods=['DELETE'])
def delete_dish(id):
    """Remove um prato"""
    dish = Dish.query.get_or_404(id)
    db.session.delete(dish)
    db.session.commit()
    return '', 204