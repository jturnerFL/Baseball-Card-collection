from asyncio.events import BaseDefaultEventLoopPolicy
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, BaseballCard, baseball_card_schema, baseball_cards_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Babe': 'Ruth'}

# Create Card
@api.route('/BaseballCards', methods = ['POST'])
@token_required
def create_baseballcard(current_user_token):
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
    cards = BaseballCard.query.filter_by(user_token = a_user).all()
    response = baseball_cards_schema.dump(cards)
    return jsonify(response)

@api.route('/BaseballCards/<id>', methods = ['GET'])
@token_required
def get_card_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        card = BaseballCard.query.get(id)
        response = baseball_card_schema.dump(card)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/BaseballCards/<id>', methods = ['POST','PUT'])
@token_required
def update_baseballcard(current_user_token,id):
    card = BaseballCard.query.get(id) 
    card.brand = request.json['brand']
    card.year = request.json['year']
    card.player = request.json['player']
    card.condition = request.json['condition']
    card.user_token = current_user_token.token

    db.session.commit()
    response = baseball_card_schema.dump(card)
    return jsonify(response)
 # Delete Card
@api.route('/BaseballCards/<id>', methods = ['DELETE'])
@token_required
def delete_baseballcard(current_user_token, id):
    card = BaseballCard.query.get(id)
    db.session.delete(card)
    db.session.commit()
    response = baseball_card_schema.dump(card)
    return jsonify(response)
