# app/db.py

import databases
import ormar
import sqlalchemy

#from .config import settings

#database = databases.Database(settings.db_url)
database = databases.Database("postgresql+psycopg2://postgres:Ez529684p3@database-1.cvjp5ekhxkye.us-east-1.rds.amazonaws.com:5432/")
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    name: str = ormar.String(max_length=128, unique=True, nullable=False)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    password: str = ormar.String(max_length=128, nullable=False)

class ModelResult(ormar.Model):
    class Meta(BaseMeta):
        tablename = "Model"

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    acuracia: float = ormar.Float(unique=False, nullable=False)
    predicao: int = ormar.Integer(unique=False, nullable=False)
    anterioridade: str = ormar.String(max_length=64, nullable=False)
    version: str = ormar.String(max_length=128, nullable=False)
# class ToDo(ormar.Model):
#     class Meta(BaseMeta):
#         tablename = "todocard"

#     id: int = ormar.Integer(primary_key=True)
#     title: str = ormar.String(max_length=128, unique=True, nullable=False)
#     content: str = ormar.String(max_length=128, unique=True, nullable=False)
#     user_id: int = ormar.Integer()

engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:Ez529684p3@database-1.cvjp5ekhxkye.us-east-1.rds.amazonaws.com:5432/")
metadata.create_all(engine)
