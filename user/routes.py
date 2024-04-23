from flask import Blueprint, Flask, request
from user.models import User

user_bp = Blueprint("user_module", __name__)


@user_bp.route("/api/user/register", methods=["GET", "POST"])
def register_user():
    return User().register()


@user_bp.route("/api/user/login", methods=["POST"])
def login_user():
    return User().login()


@user_bp.route("/api/user/logout")
def logout_user():
    return User().logout()
