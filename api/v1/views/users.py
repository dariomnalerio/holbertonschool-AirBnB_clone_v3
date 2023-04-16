#!/usr/bin/python3
''' Endpoints for User objects '''

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from console import classes


@app_views.route('/users')
def get_all_users():
    """Retrieves the list of all Users objects."""
    users = [user.to_dict()
             for user in storage.all(classes["User"]).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>')
def get_user(user_id):
    """ Retrieves a User object """
    users = storage.all(classes["User"])
    if f"User.{user_id}" in users:
        return jsonify(users[f"User.{user_id}"].to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(classes['User'], user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    try:
        req = request.get_json()
        if not req:
            abort(400, description="Not a JSON")
        if "email" not in req:
            abort(400, description="Missing email")
        if "password" not in req:
            abort(400, description="Missing password")
        user_instance = classes["User"](**req)
        storage.new(user_instance)
        storage.save()
        return user_instance.to_dict(), 201
    except Exception:
        abort(400, description="Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Updates a User object """
    user = storage.get(classes['User'], user_id)
    if user:
        try:
            req = request.get_json()
            if not req:
                abort(400, description="Not a JSON")
            for key, value in req.items():
                if key not in ["id", "email", "created_at", "updated_at"]:
                    setattr(user, key, value)
            user.save()
            return user.to_dict(), 200
        except Exception:
            abort(400, description="Not a JSON")
    else:
        abort(404)
