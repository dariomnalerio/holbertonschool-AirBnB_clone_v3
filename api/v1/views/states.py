#!/usr/bin/python3
""" Endpoints for State objects """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from console import classes


@app_views.route('/states')
def get_all_states():
    """ Retrieves the list of all State objects """
    return jsonify([state.to_dict() for state in
                    storage.all('State').values()])


@app_views.route("/states/<state_id>")
def get_state(state_id):
    """ Retrieves a State object """
    states = storage.all(classes["State"])  # get all states
    if f"State.{state_id}" in states:
        # return state by id as dict with status code 200
        return jsonify(states[f"State.{state_id}"].to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(classes['State'], state_id)  # get state by id
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200  # return empty dict with status code 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"])
def create_state():
    """Create a new state."""
    try:
        req = request.get_json()
        if not req:
            abort(400, description="Not a JSON")
        if "name" not in req:
            abort(400, description="Missing name")
        state_instance = classes["State"](**req)
        storage.new(state_instance)
        storage.save()
        return state_instance.to_dict(), 201
    except:
        abort(400, description="Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object """
    state = storage.get(classes['State'], state_id)
    if state:
        if not request.get_json():  # if request.get_json() is None
            abort(400, description="Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:  # ignore keys
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200  # return updated state
    else:
        abort(404)
