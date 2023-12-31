import os

from alembic import command
from alembic.config import Config
from flask import Flask, request
from flask import jsonify
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy_utils import database_exists, create_database

from Constants import *
from data.common.RoleData import RoleData
from data.common.RoleDelta import RoleDelta
from data.common.StudentInfoDelta import StudentInfoDelta
from data.common.UserData import UserData
from data.common.UserDelta import UserDelta
from data.services.RolesRepository import RolesRepository
from data.services.UserRepository import UserRepository
from data.services.mysql.MySqlRolesRepository import MySqlRolesRepository
from data.services.mysql.MySqlUsersRepository import MySqlUsersRepository
from data.services.mysql.MySqlUsersRepository import UserBannedException

app = Flask(__name__)

engine: Engine = create_engine(os.environ.get('MYSQL_CONNECTION_STRING'))
roles_repo: RolesRepository = MySqlRolesRepository(engine)
user_repo: UserRepository = MySqlUsersRepository(engine)


def ensure_db_created():
    if not database_exists(engine.url):
        create_database(engine.url)


# Создание ролей по умолчанию
def setup_roles_by_default():
    all_roles_names = list(map(lambda r: r.name, roles_repo.get_all_roles()))

    for role_name in SYSTEM_ROLES:
        if role_name not in all_roles_names:
            roles_repo.create_role(role_name)


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def setup_database():
    ensure_db_created()
    run_migrations()
    setup_roles_by_default()


@app.post("/create-user")
def create_user():
    try:
        json: dict = request.json

        user_data = UserData(
            name=json['name'],
            surname=json['surname'],
            tg_id=json['tgId'],
            role=RoleData(
                id=json['roleId'],
                name="None"
            ),
            student_info=None,
            score=0,
            email=json['email']
        )

        user_repo.create_user(user_data)

        return "", 200
    except IntegrityError as e:
        return jsonify({
            "msg": "User already created with these parameters"
        }), 400
    except UserBannedException:
        return jsonify({
            "msg": "User banned"
        }), 400


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

    return jsonify(users_dict), 200


@app.put("/update-user")
def update_user():
    try:
        json = request.json

        tg_id: int = int(request.args.get('tgId'))
        user_delta: UserDelta = UserDelta(
            new_name=json.get("newName"),
            new_surname=json.get("newSurname"),
            new_role_id=json.get("newRoleId"),
            student_info_delta=None if "studentInfoDelta" not in json
            else StudentInfoDelta(
                new_is_male=json["studentInfoDelta"].get("newIsMale"),
                new_room_number=json["studentInfoDelta"].get("newRoomNumber"),
                new_group_number=json["studentInfoDelta"].get("newGroupNumber"),
            ),
            new_score=json.get("newScore"),
            delta_score=json.get("deltaScore")
        )

        updated_user = user_repo.update_user(tg_id, user_delta)

        return jsonify(updated_user.to_dict()), 200
    except NoResultFound:
        return jsonify({
            "msg": "User not found"
        }), 400


@app.delete("/delete-user")
def delete_user():
    tg_id: int = int(request.args.get('tgId'))
    user_repo.delete_user(tg_id)
    return "", 200


@app.get("/get-role")
def get_role():
    try:
        role_id: int = int(request.args.get('id'))
        result = roles_repo.get_role(role_id)

        return jsonify(result.to_dict()), 200
    except NoResultFound:
        return jsonify({
            "msg": "Role not found"
        }), 400


@app.get("/get-role-by-name")
def get_role_by_name():
    try:
        role_id: str = request.args.get('name')
        result = roles_repo.get_role_by_name(role_id)

        return jsonify(result.to_dict()), 200
    except NoResultFound:
        return jsonify({
            "msg": "Role not found"
        }), 400


@app.get("/get-roles")
def get_roles():
    roles = roles_repo.get_all_roles()
    resp = []

    for role in roles:
        resp.append(role.to_dict())

    return jsonify(resp), 200


@app.delete("/delete-role")
def delete_role():
    role_id: int = int(request.args.get('id'))
    roles_repo.delete_role(role_id)
    return "", 200


@app.put("/update-role")
def update_role():
    try:
        role_id: int = int(request.args.get('id'))
        json = request.json

        delta = RoleDelta(
            new_name=json.get("newName")
        )
        result = roles_repo.update_role(role_id, delta)

        return jsonify(result.to_dict()), 200
    except NoResultFound:
        return jsonify({
            "msg": "Role not found"
        }), 200


@app.post("/ban-user")
def ban_user():
    try:
        tg_id = int(request.args.get('tgId'))
        user_repo.ban_user(tg_id)

        return "", 200
    except IntegrityError:
        return jsonify({
            "msg": "User already banned"
        }), 200


@app.delete("/unban-user")
def unban_user():
    try:
        tg_id = int(request.args.get('tgId'))
        user_repo.unban_user(tg_id)

        return "", 200
    except IntegrityError:
        return jsonify({
            "msg": "User already banned"
        }), 200


@app.get("/is-user-banned")
def is_user_banned():
    tg_id = int(request.args.get('tgId'))

    return jsonify({
        "isBanned": user_repo.is_user_banned(tg_id)
    }), 200


setup_database()

if __name__ == "__main__":
    app.run()
