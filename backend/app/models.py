from typing import Optional
from ormar import Model, fields
from pydantic import BaseModel, Field, EmailStr
from fastapi import File

class FileBase(BaseModel):
    name: str
    content: bytes



class FileCreate(FileBase):
    pass

# class File(FileBase, Model):
#     class Meta:
#         tablename = "files"

# class FileInDB(File):
#     pass

class ModelResultSchema(BaseModel):
    id : int = Field(default=None, gt=0)
    acuracia: float = Field(default=None)
    predicao: int = Field(default=None)
    anterioridade: str = Field(default=None)
    version: str = Field(default=None)
    # Configuração criada para documentação do modelo
    class Config:
        schema_extra = {
            "post_teste" : {
                "acuracia": 1.0,
                "predicao": 0.8,
                "anterioridade": "7 dias",
                "version" : "1.0.0"
            }
        }

# Classe para representar os usuários do sistema
class UserSchema(BaseModel):
    id : int = Field(default=None, gt=0)
    email : EmailStr = Field(default=None)
    name: str = Field(default=None)
    password : str = Field(default=None)
    class Config:
        schema_extra = {
            "schema_user" : {
                "email": "teste@mail.com",
                "name": "teste",
                "password":"123",
                "id": 1
            }
        }