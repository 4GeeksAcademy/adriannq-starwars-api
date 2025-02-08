from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import enum
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class Planets(db.Model):
    __tablename__ = 'Planets'
    id:int = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name:str = db.Column(db.String(250), nullable=False, unique=True)
    population:int = db.Column(db.Integer, nullable=False)
    climate:str = db.Column(db.String(250), nullable=False)
    diameter:int = db.Column(db.Integer, nullable=False)
    rotation_period:int = db.Column(db.Integer, nullable=False)
    orbital_period:int = db.Column(db.Integer, nullable=False)
    gravity:str = db.Column(db.String(250), nullable=False)
    terrain:str = db.Column(db.String(250), nullable=False)
    url:str = db.Column(db.String(250), nullable=False)
    

    def __repr__(self):
        return f"<Planet {self.name}>"
    
@dataclass
class Starships(db.Model):
    __tablename__ = 'Starships'
    id:int = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name:str = db.Column(db.String(250), nullable=False, unique=True)
    model:str = db.Column(db.String(250), nullable=False)
    starship_class:str = db.Column(db.String(250), nullable=False)
    manufacturer:str = db.Column(db.String(250), nullable=False)
    cost_in_credits:str = db.Column(db.String(250), nullable=False)
    length:int = db.Column(db.Integer, nullable=False)
    crew:str = db.Column(db.String(250), nullable=False)
    max_atmosphering_speed:str = db.Column(db.String(250), nullable=False)
    hyperdrive_rating:str = db.Column(db.String(250), nullable=False)
    MGLT:str = db.Column(db.String(250), nullable=False)
    cargo_capacity:str = db.Column(db.String(250), nullable=False)
    consumables:str = db.Column(db.String(250), nullable=False)
    url:str = db.Column(db.String(250), nullable=False)


    def __repr__(self):
        return f"<Planet {self.name}>"

@dataclass
class Films(db.Model):
    __tablename__ = 'Films'
    id:int = db.Column(db.Integer, primary_key=True, unique=True)
    title:str = db.Column(db.String(250), nullable=False, unique=True)
    episode_id:int = db.Column(db.Integer, nullable=False)
    release_date:str = db.Column(db.String(250), nullable=False)
    director:str = db.Column(db.String(250), nullable=False)
    producer:str = db.Column(db.String(250), nullable=False)
    opening_crawl:str = db.Column(db.String(250), nullable=False)
    url:str = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"<Films {self.title}>"

@dataclass
class People(db.Model):
    __tablename__ = 'People'
    id:int = db.Column(db.Integer, primary_key=True, unique=True)
    name:str = db.Column(db.String(250), nullable=False, unique=True)
    skin_color:str = db.Column(db.String(250), nullable=False)
    hair_color:str = db.Column(db.String(250), nullable=False)
    eye_color:str = db.Column(db.String(250), nullable=False)
    birth_year:str = db.Column(db.String(250), nullable=False)
    gender:str = db.Column(db.String(250), nullable=False)
    url:str = db.Column(db.String(250), nullable=False)
    height:int = db.Column(db.Integer, nullable=False)
    mass:int = db.Column(db.Integer, nullable=False)
    homeworld:str = db.Column(db.String(250), ForeignKey("Planets.name"))
   

    def __repr__(self):
        return f'<Character {self.name}>'

@dataclass
class User(db.Model):
    __tablename__ = 'User'
    id:int = db.Column(db.Integer, primary_key = True)
    username:str = db.Column(db.String(250), nullable = False, unique=True)
    first_name:str = db.Column(db.String(250), nullable = False)
    last_name:str = db.Column(db.String(250), nullable = False)
    email:str = db.Column(db.String(250),nullable = False, unique = True)
    password= db.Column(db.VARCHAR(80), nullable = False)
    is_active:bool = db.Column(db.Boolean(), unique = False)
    

class FavoriteTypeEnum(str,enum.Enum):
    Planets = "Planets"
    People = "People"
    Films = "Films"

@dataclass
class Favorites(db.Model):
    __tablename__ = 'Favorites'
    id:int = db.Column(db.Integer, primary_key=True, unique=True)
    user_id:int = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
    external_id:int = db.Column(db.Integer, nullable=False)
    name:str = db.Column(db.String(250), nullable=False)
    type:FavoriteTypeEnum = db.Column(db.Enum(FavoriteTypeEnum), nullable=False)


    def __repr__(self):
        return f"<Favorite {self.name} ({self.type.value})>"
