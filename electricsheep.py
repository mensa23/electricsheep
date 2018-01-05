from flask import Flask
from flask_mongoengine import MongoEngine

from player import player
from setting import SECRET_KEY, DATABASE_NAME

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': DATABASE_NAME
}
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(player, url_prefix='/player/api')

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()
