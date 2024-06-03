#!/usr/bin/python3
"""A view for Places_reviews objects"""


from flask import abort, request, jsonify
from api.v1.views import app_views, storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews_belonging_to_place_id(place_id):
    """list of all reviews objects of a place

    Keyword arguments:
    place_id -- the id of the place
    Return: a json representation of the review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        if 'user_id' not in data:
            abort(400, description="Missing user_id")
        user_id = data.get('user_id')
        if not storage.get(User, user_id):
            abort(404)
        if 'text' not in data:
            abort(400, description="Missing text")
        review = Review(**data)
        review.user_id = user_id
        review.place_id = place_id
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def reviews_by_id(review_id):
    """carrys out GET, PUT and DELETE requests on the returned review

    Keyword arguments:
    review_id -- the id of the review
    Return: returns the json representation of the object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'PUT':
        if not request.is_json:
            abort(400, description="Not a JSON")

        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, val in data.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, val)
        review.save()
        return jsonify(review.to_dict()), 200

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200
