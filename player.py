import re
from datetime import datetime

from flask import Blueprint, jsonify, request

from setting import TOKEN_EXPIRATION
from util import auth, InvalidAccessToken

player = Blueprint('player', __name__)


def player_validation(username, password):
    user_pattern = re.compile(r'^[a-zA-Z0-9_]{4,16}$')
    if not re.match(user_pattern, username):
        raise InvalidUsername('用户名不符合要求！')
    pass_pattern = re.compile(r'^[a-zA-Z0-9]{6,16}$')
    if not re.match(pass_pattern, password):
        raise InvalidPassword('密码不符合要求！')
    from model import Player
    p = Player.objects(username=username)
    if p:
        raise UserExisted('用户名已存在！')


@player.route('/registry', methods=['POST'])
def register():
    from model import Player
    player_payload = request.json
    username = player_payload['username']
    password = player_payload['password']
    player_validation(username=username, password=password)
    p = Player(username=username, created_date=datetime.utcnow())
    p.hash_password(password)
    p.save()
    response = dict()
    response['id'] = str(p.id)
    response['username'] = p.username
    return jsonify(response)


@player.route('/token', methods=['POST'])
def get_token():
    from model import Player
    player_payload = request.json
    username = player_payload['username']
    password = player_payload['password']
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
# Exception Handlers
##################################################
class PlayerUnauthorized(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        error_dict = dict()
        error_dict['message'] = self.message
        error_dict['error_code'] = PLAYER_UNAUTHORIZED
        return error_dict


class InvalidUsername(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        error_dict = dict()
        error_dict['message'] = self.message
        error_dict['error_code'] = INVALID_USERNAME
        return error_dict


class InvalidPassword(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        error_dict = dict()
        error_dict['message'] = self.message
        error_dict['error_code'] = INVALID_PASSWORD
        return error_dict


class UserExisted(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        error_dict = dict()
        error_dict['message'] = self.message
        error_dict['error_code'] = INVALID_PASSWORD
        return error_dict


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


@player.errorhandler(InvalidUsername)
def handle_invalid_token(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@player.errorhandler(UserExisted)
def handle_invalid_token(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


##################################################
# ERROR CODES
##################################################
PLAYER_UNAUTHORIZED = 400000
INVALID_USERNAME = 400001
INVALID_PASSWORD = 400002
USER_EXISTED = 400003
