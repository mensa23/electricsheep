from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context

from electricsheep import db, app
from setting import TOKEN_EXPIRATION


class Player(db.Document):
    username = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    created_date = db.DateTimeField(required=True)
    uto = db.IntField(default=0)
    mps = db.IntField(default=0)
    health = db.DecimalField(default=100)

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
    key = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    price_uto = db.IntField(default=0)
    price_mps = db.IntField(default=0)


class Chip(db.Document):
    key = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    price_uto = db.IntField(default=0)
    price_mps = db.IntField(default=0)
    level = db.IntField(default=1)
    damage_buff = db.DecimalField(default=0)
    shield_buff = db.DecimalField(default=0)


class Plugin(db.Document):
    key = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    price_uto = db.IntField(default=0)
    price_mps = db.IntField(default=0)
    level = db.IntField(default=1)
    damage = db.DecimalField(default=0)
    shield = db.DecimalField(default=0)


class City(db.Document):
    key = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    force_id = db.StringField(required=True)
    battle_ratio = db.DecimalField(default=0)
    force_ratio = db.DictField()
    north_city_id = db.StringField()
    south_city_id = db.StringField()
    west_city_id = db.StringField()
    east_city_id = db.StringField()


class Force(db.Document):
    key = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    member = db.IntField(default=0)
    camp_id = db.StringField(required=True)


class Science(db.Document):
    key = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    level = db.IntField(default=1)
    anti_level = db.IntField(default=1)
