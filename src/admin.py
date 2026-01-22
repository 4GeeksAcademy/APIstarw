import os
from flask_admin import Admin
from models import db, User, Planets, Characters, Starships, FavoriteCharacters, FavoritePlanets, FavoriteStarships
from flask_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
        column_list = ("id", "username", "email")

class PlanetAdmin(ModelView):
        column_list = ("id", "planets_name")

class CharactersAdmin(ModelView):
        column_list = ("id", "character_name", "planets_id")
        form_columns = ("character_name", "planet")

class StarshipsAdmin(ModelView):
        column_list = ("id", "starships_name")
        form_excluded_columns = ("favorited_by",)

class FavoriteCharactersAdmin(ModelView):
        column_list = ("id", "user_id", "characters_id")

class FavoritePlanetsAdmin(ModelView):
        column_list = ("id", "user_id", "planet_id")

class FavoriteStarshipAdmin(ModelView):
        column_list = ("id", "user_id", "starships_id")
        


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(PlanetAdmin(Planets, db.session))
    admin.add_view(CharactersAdmin(Characters, db.session))
    admin.add_view(StarshipsAdmin(Starships, db.session))
    admin.add_view(FavoriteCharactersAdmin(FavoriteCharacters, db.session))
    admin.add_view(FavoritePlanetsAdmin(FavoritePlanets, db.session))
    admin.add_view(FavoriteStarshipAdmin(FavoriteStarships, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
