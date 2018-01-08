from flask import Blueprint, jsonify

from util import auth

resource = Blueprint('resource', __name__)


@resource.route('/resources/', methods=['GET'])
@auth.login_required
def get_players():
    return jsonify({})
