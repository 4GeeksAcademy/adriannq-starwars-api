"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Films, Planets, People,Starships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

FavoriteType=["People","Planets","Films"]

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/characters', methods=['GET'])
def get_all_characters():
    all_characters= People.query.all()
    return jsonify(all_characters), 200

@app.route("/characters/<int:id>", methods=["GET"])
def  get_single_character(id):
    character = People.query.get(id)
    response_body = character
    return jsonify(response_body), 200

@app.route('/films', methods=['GET'])
def get_films():
    all_films= Films.query.all()
    return jsonify(all_films), 200

@app.route("/films/<int:id>", methods=["GET"])
def  get_single_film(id):
    film = Films.query.get(id)
    response_body = film
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets= Planets.query.all()
    
    return jsonify(all_planets), 200

@app.route("/planets/<int:id>", methods=["GET"])
def  get_single_planet(id):
    planet = Planets.query.get(id)
    return jsonify(planet), 200

@app.route('/starships', methods=['GET'])
def get_starships():
    all_planets= Starships.query.all()
    
    return jsonify(all_planets), 200

@app.route("/starships/<int:id>", methods=["GET"])
def  get_single_starship(id):
    planet = Starships.query.get(id)
    return jsonify(planet), 200

@app.route('/user', methods=['GET'])
def get_users():
    all_users= User.query.all()
    return jsonify(all_users), 200

@app.route("/user/<int:user_id>", methods=["GET"])
def  get_single_user(user_id):
    user = User.query.get(user_id)
    response_body = user
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return jsonify(favorites), 200


@app.route("/favorites/<int:id>", methods=["GET"])
def  get_single_favorite(id):
    favorite = Favorites.query.get(id)
    response_body = favorite
    return jsonify(response_body), 200

@app.route("/user/<int:user_id>/favorites", methods=["POST"])
def add_favorite(user_id):
    data = request.get_json()
    required_fields=["name","type","external_id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error":"missing required fields"}),400
    if not (data["type"] in FavoriteType):
        return jsonify({"error":"type not valide"})
    if Favorites.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Resource already favourited"}), 400

    new_favorite=Favorites(
        user_id=data["user_id"],
        external_id=data["external_id"],
        name=data["name"],
        type=data["type"]
        )
   
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite), 201

@app.route("/user/<int:user_id>/favorites/<int:id>", methods=["DELETE"])
def  delete_favorite(id,user_id):
    
    favorite = Favorites.query.get(id)

    db.session.delete(favorite)
    db.session.commit()
    return jsonify("Favorite deleted successfully"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
