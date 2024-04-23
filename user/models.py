from flask import Flask, jsonify, request, session
from passlib.hash import pbkdf2_sha256 as sha256
from data.connector import database
from bson import json_util
import json


# JSON Parser
def parse_json(data):
    return json.loads(json_util.dumps(data))


class User:

    # Start a new session
    def start_session(self, user):
        del user["password"]
        del user["username"]
        user["_id"] = parse_json(user["_id"])
        user["isLogged"] = True
        session["logged_in"] = True
        session["user"] = user
        session.permanent = True
        return jsonify(user), 200

    def register(self):

        user = {
            "username": request.json["username"],
            "password": request.json["password"],
        }

        # Encrypt the password
        user["password"] = sha256.hash(user["password"])

        # Check if the user already exists
        if database.users.find_one({"username": user["username"]}):
            return "User already exists", 400

        # Insert the user into the database
        if database.users.insert_one(user):
            return self.start_session(user)

        return "Failed to create user", 500

    def login(self):
        user = database.users.find_one({"username": request.json["username"]})

        if user and sha256.verify(request.json["password"], user["password"]):
            return self.start_session(user)

        return jsonify("Invalid username or password"), 401

    def logout(self):
        session.clear()
        return jsonify("Logged out"), 200
