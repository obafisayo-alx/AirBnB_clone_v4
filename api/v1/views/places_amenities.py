#!/usr/bin/python3
"""A view for linking Place objects and Amenity objects"""

from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities",
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities_for_place(place_id):
    """Retrieves the list of all Amenity objects associated with a Place
    Args:
        place_id (str): The ID of the Place
    Returns:
        JSON response containing the list of Amenity objects
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # Place not found, return 404 error

    amenities_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def manage_amenity_for_place(place_id, amenity_id):
    """Deletes or links an Amenity object to a Place
    Args:
        place_id (str): The ID of the Place
        amenity_id (str): The ID of the Amenity
    Returns:
        JSON response with appropriate status code
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)  # Place or Amenity not found, return 404 error

    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)  # Amenity not linked to the Place, return 404 error
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'POST':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200  # Amenity already linked
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
