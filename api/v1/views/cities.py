#!/usr/bin/python3
""" Endpoints for City objects """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from console import classes


@app_views.route('/states/<state_id>/cities')
def get_all_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(classes["State"], state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    else:
        abort(404)


@app_views.route("/cities/<city_id>")
def get_city(city_id):
    """ Retrieves a City object """
    cities = storage.all(classes["City"])
    if f"City.{city_id}" in cities:
        return jsonify(cities[f"City.{city_id}"].to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(classes['City'], city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Create a new city."""
    if not storage.get(classes["State"], state_id):
        abort(404)
    else:
        try:
            req = request.get_json()
            if not req:
                abort(400, description="Not a JSON")
            if "name" not in req:
                abort(400, description="Missing name")
            city_instance = classes["City"](**req)
            city_instance.state_id = state_id
            storage.new(city_instance)
            storage.save()
            return city_instance.to_dict(), 201
        except:
            abort(400, description="Not a JSON")


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Updates a City object """
    city_instance = storage.get(classes['City'], city_id)
    if city_instance:
        if not request.get_json(): # if request.get_json() is None
            abort(400, description="Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']: # ignore these keys
                setattr(city_instance, key, value)
        storage.save()
        return jsonify(city_instance.to_dict()), 200 # return updated city
    else:
        abort(404)
