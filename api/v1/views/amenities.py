#!/usr/bin/python3
"""
view of amenities
"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity



@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves a list of all amenities"""
    all_amenities = storage.all('Amenity')
    amenities_list = all_amenities.values()
    amenities_json = []
    for amenity in amenities_list:
        amenities_json.append(amenity.to_dict())
    return jsonify(amenities_json)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """retrieves amenity obj"""
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    return jsonify(my_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """deletes a amenity"""
    delete_amenity = storage.get('Amenity', amenity_id)
    if not delete_amenity:
        abort(404)
    else:
        delete_amenity.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """post a new amenity"""
    new_amenity = request.get_json()
    if new_amenity is None:
        abort(400, 'Not a JSON')
    if 'name' not in new_amenity:
        abort(400, 'Missing name')
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """Update a amenity"""
    req_amenity = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    mod_amenity = storage.get('Amenity', amenity_id)
    if mod_amenity is None:
        abort(404)
    for key in req_amenity:
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_amenity, key, req_amenity[key])
    storage.save()
    return jsonify(mod_amenity.to_dict()), 200
