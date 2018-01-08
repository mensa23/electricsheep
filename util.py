from flask_httpauth import HTTPTokenAuth

from exception import InvalidAccessToken

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    from model import Player
    p = Player.verify_auth_token(token)
    if not p:
        raise InvalidAccessToken('无效的授权！')
    return True
