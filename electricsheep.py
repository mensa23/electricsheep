from flask import Flask
from flask_mongoengine import MongoEngine

from player import player

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'electricsheep'
}
app.config['SECRET_KEY'] = 'ZWxlY3RyaWNzaGVlcEB3d3cuc3RhcnVuY2xlcy5jb20='
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(player, url_prefix='/player/api')

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()
