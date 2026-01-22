from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    #relationship
    favorite_planets: Mapped[List["FavoritePlanets"]] = relationship(back_populates="user")
    favorite_characters: Mapped[List["FavoriteCharacters"]] = relationship(back_populates="user")
    favorite_starships: Mapped[List["FavoriteStarships"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):

    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    planets_name: Mapped[str] = mapped_column(String(120), unique=True)
    
    #relationship
    favorited_by: Mapped[List["FavoritePlanets"]] = relationship(back_populates="planet")
    characters: Mapped[List["Characters"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "planets_name": self.planets_name,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    character_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

#relationship
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    planet: Mapped["Planets"] = relationship(back_populates="characters")
    favorited_by: Mapped[List["FavoriteCharacters"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "planets_id": self.planets_id
            # do not serialize the password, its a security breach
        }

class Starships(db.Model):
    __tablename__ = "starships"

    id: Mapped[int] = mapped_column(primary_key=True)
    starships_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    #relationship
    favorited_by: Mapped[List["FavoriteStarships"]] = relationship(back_populates="starship")



    def serialize(self):
        return {
            "id": self.id,
            "starships_name": self.starships_name,
            # do not serialize the password, its a security breach
        }
class FavoritePlanets(db.Model):

    __tablename__ = "favorite_planets"
    id: Mapped[int] = mapped_column(primary_key=True)

    #relationship

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planets"] = relationship(back_populates="favorited_by")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            # do not serialize the password, its a security breach
        }
class FavoriteCharacters(db.Model):

    __tablename__ = "favorite_characters"

    id: Mapped[int] = mapped_column(primary_key=True)

    #relationship

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    characters_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character: Mapped["Characters"] = relationship(back_populates="favorited_by")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "characters_id": self.characters_id,
            # do not serialize the password, its a security breach
        }

class FavoriteStarships(db.Model):

    __tablename__ = "favorite_starships"
    id: Mapped[int] = mapped_column(primary_key=True)

    #relationship

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), )
    starships_id: Mapped[int] = mapped_column(ForeignKey("starships.id"))
    user: Mapped["User"] = relationship(back_populates="favorite_starships")    
    starship: Mapped["Starships"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starships_id": self.starships_id,
            # do not serialize the password, its a security breach
        }