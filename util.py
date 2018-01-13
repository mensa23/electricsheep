from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth()


class InvalidAccessToken(Exception):
    status_code = 401

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        error_dict = dict()
        error_dict['message'] = self.message
        error_dict['error_code'] = INVALID_ACCESS_TOKEN
        return error_dict


@auth.verify_token
def verify_token(token):
    from model import Player
    p = Player.verify_auth_token(token)
    if not p:
        raise InvalidAccessToken('无效的授权！')
    return True


##################################################
# ERROR CODES
##################################################
INVALID_ACCESS_TOKEN = 401000
