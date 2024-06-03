#!/usr/bin/python3
"""index file"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """
    status route
    :return: response with json
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stat():
    """
    retrieves number of each object type
    Return: return response with json
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp
