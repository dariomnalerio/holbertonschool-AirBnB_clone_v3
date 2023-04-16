#!/usr/bin/python3
""" Endpoints for Place objects """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from console import classes


@app_views.route('/cities/<city_id>/places')
def get_all_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    cities = storage.all(classes["City"])
    if f"City.{city_id}" not in cities:
        abort(404)
    else:
        places = [place.to_dict()
                  for place in storage.all(classes["Place"]).values()
                  if place.city_id == city_id]
        return jsonify(places)


@app_views.route('/places/<place_id>')
def get_place(place_id):
    """ Retrieves a Place object """
    places = storage.all(classes["Place"])
    if f"Place.{place_id}" not in places:
        abort(404)
    else:
        return jsonify(places[f"Place.{place_id}"].to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a Place object """
    places = storage.all(classes["Place"])
    if f"Place.{place_id}" not in places:
        abort(404)
    else:
        storage.delete(places[f"Place.{place_id}"])
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Create a new place."""
    cities = storage.all(classes["City"])
    if f"City.{city_id}" not in cities:
        abort(404)
    try:
        req = request.get_json()
        if not req:
            abort(400, description="Not a JSON")
        if "user_id" not in req:
            abort(400, description="Missing user_id")
        if "name" not in req:
            abort(400, description="Missing name")
        req["city_id"] = city_id
        place_instance = classes["Place"](**req)
        storage.new(place_instance)
        storage.save()
        return place_instance.to_dict(), 201
    except Exception:
        abort(400, description="Not a JSON")


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(classes['Place'], place_id)
    if place:
        try:
            req = request.get_json()
            if not req:
                abort(400, description="Not a JSON")
            for key, value in req.items():
                if key not in ['id', 'user_id', 'city_id', 'created_at',
                               'updated_at']:
                    setattr(place, key, value)
            storage.save()
            return place.to_dict(), 200
        except Exception:
            abort(400, description="Not a JSON")
