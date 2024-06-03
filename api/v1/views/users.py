#!/usr/bin/python3
"""A view for Users objects"""


from xml.etree.ElementInclude import include
from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Handles GET and POST requests for /users route.
    Return: a list of users or created user
    """
    if request.method == 'GET':
        users_list = [user.to_dict()
                      for user in storage.all(User).values()]
        return jsonify(users_list)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if 'email' not in data:
            abort(400, "Missing email")
        if 'password' not in data:
            abort(400, "Missing password")
        new_user = User(**data)
        new_user.save()
        res = jsonify(new_user.to_dict())
        res.status_code = 201
        return res


@app_views.route("/users/<user_id>",
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def user_by_id(user_id):
    """Handles GET, PUT and DELETE request for /users/<user_id>

    Keyword arguments:
    user_id -- this is the user id
    Return: returns the individual user gotten by the id or error
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, val in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, val)
        user.save()
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200
