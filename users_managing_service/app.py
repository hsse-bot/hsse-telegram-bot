import os

from flask import Flask, request
from flask import jsonify
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import NoResultFound

from data.common.RoleData import RoleData
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
    json: dict = request.json
    
    user_data = UserData(
        name=json['name'],
        surname=json['surname'],
        tg_id=json['tgId'],
        role=RoleData(
            id=json['roleId']
        )
    )

    user_repo.create_user(user_data)

    return 200


@app.get("/get-user")
def get_user():
    try:
        tg_id: int = int(request.args.get('tgId'))
        result = user_repo.get_user(tg_id)

        if result:
            return jsonify(result.to_dict())
    except NoResultFound:
        return jsonify({
            "msg": "User not found"
        }), 400


@app.get("/get-all-users")
def get_all_users():
    users = user_repo.get_all_users()
    users_dict = []

    for user in users:
        users_dict.append(user.to_dict())

    return jsonify(users)


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
