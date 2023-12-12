from flask import Flask

app = Flask(__name__)


@app.post("/create-user")
def create_user():
    raise NotImplementedError()


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
