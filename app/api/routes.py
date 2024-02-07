from flask import Blueprint, request, jsonify, render_template
from app.helpers import token_required
from app.models import db, User, Inventory, inventory_schema, inventories_schema
from app.forms import UserInventoryForm, UserLoginForm

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

# @api.route('/data')
# def viewdata():
#     data = get_contact()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/inventory', methods=['POST'])
@token_required
def create_inventory(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token

    inventory_item = Inventory(make, model, year, color, user_token=user_token)

    db.session.add(inventory_item)
    db.session.commit()

    response = inventory_schema.dump(inventory_item)
    return jsonify(response)

@api.route('/inventory', methods=['GET'])
@token_required
def get_inventory(current_user_token):
    a_user = current_user_token.token
    inventory_items = Inventory.query.filter_by(user_token=a_user).all()
    response = inventories_schema.dump(inventory_items)
    return jsonify(response)

@api.route('/inventory/<id>', methods=['GET'])
@token_required
def get_inventory_item(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        inventory_item = Inventory.query.get(id)
        response = inventory_schema.dump(inventory_item)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}), 401

@api.route('/inventory/<id>', methods=['PUT'])
@token_required
def update_inventory(current_user_token, id):
    inventory_item = Inventory.query.get(id)
    inventory_item.make = request.json['make']
    inventory_item.model = request.json['model']
    inventory_item.year = request.json['year']
    inventory_item.color = request.json['color']
    inventory_item.user_token = current_user_token.token

    db.session.commit()
    response = inventory_schema.dump(inventory_item)
    return jsonify(response)

@api.route('/inventory/<id>', methods=['DELETE'])
@token_required
def delete_inventory(current_user_token, id):
    inventory_item = Inventory.query.get(id)
    db.session.delete(inventory_item)
    db.session.commit()
    response = inventory_schema.dump(inventory_item)
    return jsonify(response)