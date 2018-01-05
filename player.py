from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_httpauth import HTTPTokenAuth

from exception import PlayerUnauthorized

player = Blueprint('player', __name__)

auth = HTTPTokenAuth()


@player.route('/registry', methods=['POST'])
def register():
    from model import Player
    player_payload = request.json
    username = player_payload['username']
    password = player_payload['password']
    p = Player(username=username, created_date=datetime.utcnow())
    p.hash_password(password)
    p.save()
    return jsonify(p)


@player.route('/token', methods=['POST'])
def get_token():
    from model import Player
    username = request.args.get('username')
    password = request.args.get('password')
    p = Player.objects(username=username).get()
    if not p or not p.verify_password(password):
        raise PlayerUnauthorized('获取权限失败！').to_dict()
    response = dict()
    response['access_token'] = p.generate_auth_token().decode()
    response['expires_in'] = 600
    return jsonify(response)


@player.route('/players/', methods=['GET'])
@auth.login_required
def get_player():
    return None


@auth.verify_token
def verify_token(token):
    from model import Player
    p = Player.verify_auth_token(token)
    if not p:
        return False
    return True
