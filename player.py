from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_httpauth import HTTPTokenAuth

from exception import PlayerUnauthorized, InvalidAccessToken
from setting import TOKEN_EXPIRATION

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
        raise PlayerUnauthorized('获取权限失败！')
    response = dict()
    response['access_token'] = p.generate_auth_token().decode()
    response['expires_in'] = TOKEN_EXPIRATION
    return jsonify(response)


@player.route('/players/', methods=['GET'])
@auth.login_required
def get_player():
    return jsonify({})


##################################################
# Utils
##################################################
@auth.verify_token
def verify_token(token):
    from model import Player
    p = Player.verify_auth_token(token)
    if not p:
        raise InvalidAccessToken('无效的授权！')
    return True


##################################################
# Exception Handlers
##################################################
@player.errorhandler(PlayerUnauthorized)
def handle_player_unauthorized(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@player.errorhandler(InvalidAccessToken)
def handle_invalid_token(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
