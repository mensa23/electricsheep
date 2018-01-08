from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context

from electricsheep import db, app
from setting import TOKEN_EXPIRATION


class Player(db.Document):
    username = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    created_date = db.DateTimeField(required=True)
    uto = db.FloatField(default=0.0)
    mps = db.IntField(default=0)

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=TOKEN_EXPIRATION):
        secret_key = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return secret_key.dumps({'id': str(self.id)})

    @staticmethod
    def verify_auth_token(token):
        secret_key = Serializer(app.config['SECRET_KEY'])
        try:
            data = secret_key.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        player = Player.objects(id=data['id']).get()
        return player


class Resource(db.Document):
    name = db.StringField(required=True, unique=True)
    description = db.StringField(required=True)
    price_uto = db.FloatField(default=0)
    price_mps = db.IntField(default=0)
    level = db.IntField(default=1)
