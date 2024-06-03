#!/usr/bin/python3
"""A view for amenities objects"""


from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """Handles GET and POST requests for /amenities route.
    Return: a list of amenities
    """
    if request.method == 'GET':
        amenities_list = [amenity.to_dict()
                          for amenity in storage.all(Amenity).values()]
        return jsonify(amenities_list)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if 'name' not in data:
            abort(400, "Missing name")
        new_amenity = Amenity(**data)
        new_amenity.save()
        res = jsonify(new_amenity.to_dict())
        res.status_code = 201
        return res


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """Handles GET, PUT and DELETE request for /amenities/<amenity_id>

    Keyword arguments:
    amenity_id -- this is the amenity id
    Return: returns the individual amenity gotten by the id or error
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, val in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, val)
        amenity.save()
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200
