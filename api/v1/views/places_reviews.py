#!/usr/bin/python3
""" Endpoints for Place_review objects """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from console import classes


@app_views.route('/places/<place_id>/reviews')
def get_all_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    places = storage.all(classes["Place"])
    if f"Place.{place_id}" not in places:
        abort(404)
    else:
        reviews = [review.to_dict()
                   for review in storage.all(classes["Review"]).values()
                   if review.place_id == place_id]
        return jsonify(reviews)


@app_views.route('/reviews/<review_id>')
def get_review(review_id):
    """ Retrieves a Review object """
    reviews = storage.all(classes["Review"])
    if f"Review.{review_id}" not in reviews:
        abort(404)
    else:
        return jsonify(reviews[f"Review.{review_id}"].to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a Review object """
    reviews = storage.all(classes["Review"])
    if f"Review.{review_id}" not in reviews:
        abort(404)
    else:
        storage.delete(reviews[f"Review.{review_id}"])
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Create a new review."""
    places = storage.all(classes["Place"])
    if f"Place.{place_id}" not in places:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, description="Not a JSON")
    if "user_id" not in req:
        abort(400, description="Missing user_id")
    if "text" not in req:
        abort(400, description="Missing text")
    users = storage.all(classes["User"])
    user_id = req["user_id"]
    if f"User.{user_id}" not in users:
        abort(404)
    req["place_id"] = place_id
    new_review = classes["Review"](**req)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ Updates a Review object """
    reviews = storage.all(classes["Review"])
    if f"Review.{review_id}" not in reviews:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, description="Not a JSON")
    for key, value in req.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(reviews[f"Review.{review_id}"], key, value)
    storage.save()
    return jsonify(reviews[f"Review.{review_id}"].to_dict()), 200
