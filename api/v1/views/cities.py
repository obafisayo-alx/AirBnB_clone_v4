#!/usr/bin/python3
"""A view for cities objects"""


from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_by_state(state_id):
    """Handles GET and POST requests for cities belonging to a particular state
    Args:
        state_id (str): The ID of the state whose cities need to be retrieved
    Returns:
        JSON response containing cities data
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        if 'name' not in data:
            abort(400, description="Missing name")
        city = City(**data)
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def cities_by_id(city_id):
    """Handles GET, PUT, and DELETE requests for a specific city
    Args:
        city_id (str): The ID of the city to be retrieved
    Returns:
        JSON response containing city data
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'PUT':
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, val in data.items():
            if key not in ['id', 'state_id', 'updated_at', 'created_at']:
                setattr(city, key, val)
        city.save()
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200
