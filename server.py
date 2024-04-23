from functools import wraps
from flask import Flask, request, jsonify, send_file, session
from data.connector import (
    create_new_flix,
    get_all_flix,
    get_one_flix,
    replace_flix,
    delete_flix,
)
from bson import json_util
import json, os
from user.routes import user_bp
from datetime import timedelta

# App settings
app = Flask(__name__, static_folder="public", static_url_path="")
app.register_blueprint(user_bp)
app.secret_key = os.environ.get("LOCALFLIX_SECRET")
app.permanent_session_lifetime = timedelta(days=30)


# JSON Parser
def parse_json(data):
    return json.loads(json_util.dumps(data))


# Decorators
# Require login to access the API
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in") is None:
            return "Unauthorized", 401
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    return send_file("public\\index.html")


@app.route("/api")
@login_required
def get_all():
    data = get_all_flix()
    if data == None:
        return "Internal server error", 500
    flix = []
    for document in data:
        # TypeError: ObjectId('') is not JSON serializable
        # https://stackoverflow.com/a/18405626
        document = parse_json(document)
        flix.append(document)
    return jsonify(flix)


@app.route("/api/find/")
@login_required
def get_one():
    req = request.json
    if req["id"] != "":
        id = req["id"]
        data = get_one_flix(id)
        if data == None:
            return "Not found", 404
    else:
        return "Bad request", 400
    data = parse_json(data)
    return jsonify(data)


@app.route("/api/new", methods=["POST"])
@login_required
def add_new_flix():
    req = request.json
    success = create_new_flix(req)
    if success == None:
        return "Internal server error", 500
    return "Success", 201


@app.route("/api/update", methods=["PUT"])
@login_required
def edit_flix():
    req = request.json
    if req["id"] != "":
        id = req["id"]
        success = replace_flix(req, id)
        if success == None:
            return "Internal server error", 500
        return "Success", 200


@app.route("/api/delete", methods=["DELETE"])
@login_required
def remove_flix():
    req = request.json
    if req["id"] != "":
        id = req["id"]
        success = delete_flix(id)
        if success == None:
            return "Internal server error", 500
        return "Success", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
