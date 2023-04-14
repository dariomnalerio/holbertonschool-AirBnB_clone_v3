#!/usr/bin/python3
""" Endpoints for State objects """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states')
def get_all_states():
    """ Retrieves the list of all State objects """
    return jsonify([state.to_dict() for state in
                    storage.all('State').values()])


@app_views.route('/states/<state_id>')
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get('State', state_id)  # get state by id
    if state:
        return jsonify(state.to_dict())  # return state
    else:
        abort(404)  # return 404 if state is None


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get('State', state_id)  # get state by id
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200  # return empty dict with status code 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Creates a State """
    if not request.get_json():  # if request.get_json() is None
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201  # return new state


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a State object """
    state = storage.get('State', state_id)
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
