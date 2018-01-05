class PlayerUnauthorized(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        error_dict = dict()
        error_dict['message'] = self.message
        return error_dict


class InvalidAccessToken(Exception):
    status_code = 401

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        error_dict = dict()
        error_dict['message'] = self.message
        return error_dict
