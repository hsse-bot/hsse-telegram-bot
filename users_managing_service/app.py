import os

from flask import Flask, request
from sqlalchemy import Engine, create_engine

from data.common.UserData import UserData
from data.services.RolesRepository import RolesRepository
from data.services.UserRepository import UserRepository
from data.services.mysql.MySqlRolesRepository import MySqlRolesRepository
from data.services.mysql.MySqlUsersRepository import MySqlUsersRepository

app = Flask(__name__)

engine: Engine = create_engine(os.environ.get('MYSQL_CONNECTION_STRING'))
roles_repo: RolesRepository = MySqlRolesRepository(engine)
user_repo: UserRepository = MySqlUsersRepository(engine)


@app.post("/create-user")
def create_user():
    deserialized = request.get_json()
    
    user_data = UserData(
        name=deserialized['name'],
        surname=deserialized['surname'],
        tg_id=deserialized['tg_id']
    )
    
    user_repo.create_user()


@app.get("/get-user")
def get_user():
    raise NotImplementedError()


@app.get("/get-all-users")
def get_all_users():
    raise NotImplementedError()


@app.put("/update-user")
def update_user():
    raise NotImplementedError()


@app.delete("/delete-user")
def delete_user():
    raise NotImplementedError()


@app.get("/get-role")
def get_role():
    raise NotImplementedError()


@app.get("/get-role-by-name")
def get_role_by_name():
    raise NotImplementedError()


@app.get("/get-roles")
def get_roles():
    raise NotImplementedError()


if __name__ == '__main__':
    app.run()
