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
from models import db, User, Planets, Characters, Starships, FavoriteCharacters, FavoritePlanets, FavoriteStarships
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import joinedload
#from models import Person

CURRENT_USER_ID = 1

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/user', methods=['GET'])
def get_user():

    all_user = db.session.execute(select(User)).scalars().all()
    result = list(map( lambda user:user.serialize(), all_user))

    return jsonify(result), 200

@app.route('/user/<int:user_id>', methods=['GET']) 
def get_users(user_id):
    user = db.session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    if user is None:
        return jsonify("User not found"), 404
    return jsonify(user.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = db.session.execute(select(Planets)).scalars().all()
    result = list(map( lambda planets:planets.serialize(), all_planets))

    return jsonify(result), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    planet = db.session.execute(select(Planets).where(Planets.id == planets_id)).scalar_one_or_none()

    if planet is None:
        return jsonify("Planet not found"), 404
    
    return jsonify(planet.serialize()), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = db.session.execute(select(Characters)).scalars().all()
    result = list(map( lambda characters:characters.serialize(), all_characters))
  
    return jsonify(result), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_character(characters_id):
    character = db.session.execute(select(Characters).where(Characters.id == characters_id)).scalar_one_or_none()

    if character is None:
        return jsonify("Character not found"), 404
    
    return jsonify(character.serialize()), 200

@app.route('/starships', methods=['GET'])
def get_starships():
    all_starships = db.session.execute(select(Starships)).scalars().all()
    result = list(map( lambda starships:starships.serialize(), all_starships))
  
    return jsonify(result), 200

@app.route('/starships/<int:starships_id>', methods=['GET'])
def get_starship(starships_id):
    starship = db.session.execute(select(Starships).where(Starships.id == starships_id)).scalar_one_or_none()

    if starship is None:
        return jsonify("Starship not found"), 404
    
    return jsonify(starship.serialize()), 200

@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    fav_planets = db.session.execute(select(FavoritePlanets).where(FavoritePlanets.user_id == CURRENT_USER_ID).options(joinedload(FavoritePlanets.planet))).scalars().all()
    fav_characters = db.session.execute(select(FavoriteCharacters).where(FavoriteCharacters.user_id == CURRENT_USER_ID).options(joinedload(FavoriteCharacters.character))).scalars().all()

    result = {
        "favorite_planets": [
            {
                "id": fp.id,
                "planet_id": fp.planet_id,
                "planet": fp.planet.serialize() if fp.planet else None
            } 
            for fp in fav_planets
        ],
        "favorite_people": [
            {
                "id": fc.id,
                "characters_id": fc.characters_id,
                "character": fc.character.serialize() if fc.character else None
            } 
            for fc in fav_characters 
        ]
    }
    return jsonify(result), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def favorite_people(people_id):
    #check character exist
    character = db.session.execute(select(Characters).where(Characters.id == people_id)).scalar_one_or_none()

    if character is None:
        return jsonify("Character not found"), 404
    #check if favorited already exist
    existing_fav = db.session.execute(select(FavoriteCharacters).where(FavoriteCharacters.user_id == CURRENT_USER_ID, FavoriteCharacters.characters_id == people_id)).scalar_one_or_none()

    if existing_fav is not None:
        return jsonify("Character already favorited"), 409
    #create favorite
    new_fav = FavoriteCharacters(user_id=CURRENT_USER_ID, characters_id=people_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 201

@app.route('/favorite/planet/<int:planets_id>', methods=['POST'])
def favorite_planet(planets_id):
    #check planet exist
    planet = db.session.execute(select(Planets).where(Planets.id == planets_id)).scalar_one_or_none()

    if planet is None:
        return jsonify("Planet not found"), 404
    #check if favorited already exist
    existing_favplanet = db.session.execute(select(FavoritePlanets).where(FavoritePlanets.user_id == CURRENT_USER_ID, FavoritePlanets.planet_id == planets_id)).scalar_one_or_none()

    if existing_favplanet is not None:
        return jsonify("Planet already favorited"), 409
    #create favorite
    new_favplanet = FavoritePlanets(user_id=CURRENT_USER_ID, planet_id=planets_id)
    db.session.add(new_favplanet)
    db.session.commit()

    return jsonify(new_favplanet.serialize()), 201

@app.route('/favorite/starship/<int:starships_id>', methods=['POST'])
def favorite_starship(starships_id):
    #check Startship exist
    starship = db.session.execute(select(Starships).where(Starships.id == starships_id)).scalar_one_or_none()

    if starship is None:
        return jsonify("Starship not found"), 404
    #check if favorited already exist
    existing_favstarship = db.session.execute(select(FavoriteStarships).where(FavoriteStarships.user_id == CURRENT_USER_ID, FavoriteStarships.starships_id == starships_id)).scalar_one_or_none()

    if existing_favstarship is not None:
        return jsonify("Starship already favorited"), 409
    #create favorite
    new_favstarship = FavoriteStarships(user_id=CURRENT_USER_ID, starships_id=starships_id)
    db.session.add(new_favstarship)
    db.session.commit()

    return jsonify(new_favstarship.serialize()), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
