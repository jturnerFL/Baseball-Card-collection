from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, BaseballCard, baseball_card_schema, baseball_cards_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Babe': 'Ruth'}

@api.route('/BaseballCards', methods = ['POST'])
@token_required
def create_BaseballCard(current_user_token):
    brand = request.json['brand']
    year = request.json['year']
    player = request.json['player']
    condition = request.json['condition']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    card = BaseballCard(brand, year, player, condition, user_token = user_token )

    db.session.add(card)
    db.session.commit()

    response = baseball_card_schema.dump(card)
    return jsonify(response)

@api.route('/BaseballCards', methods = ['GET'])
@token_required
def get_card(current_user_token):
    a_user = current_user_token.token
    BaseballCard = BaseballCard.query.filter_by(user_token = a_user).all()
    response = baseball_card_schema.dump(BaseballCard)
    return jsonify(response)

@api.route('/BaseballCards/<id>', methods = ['GET'])
@token_required
def get_card_two(BaseballCard_user_token, id):
    fan = BaseballCard_user_token.token
    if fan == BaseballCard_user_token.token:
        BaseballCards = BaseballCard.query.get(id)
        response = baseball_cards_schema.dump(BaseballCard)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/BaseballCards/<id>', methods = ['POST','PUT'])
@token_required
def update_BaseballCard(current_user_token,id):
    BaseballCard = BaseballCard.query.get(id) 
    BaseballCard.brand = request.json['brand']
    BaseballCard.year = request.json['year']
    BaseballCard.player = request.json['player']
    BaseballCard.condition = request.json['condition']
    BaseballCard.user_token = current_user_token.token

    db.session.commit()
    response = baseball_card_schema.dump(BaseballCard)
    return jsonify(response)

@api.route('/BaseballCards/<id>', methods = ['DELETE'])
@token_required
def delete_BaseballCard(current_user_token, id):
    BaseballCard = BaseballCard.query.get(id)
    db.session.delete(BaseballCard)
    db.session.commit()
    response = baseball_card_schema.dump(BaseballCard)
    return jsonify(response)
