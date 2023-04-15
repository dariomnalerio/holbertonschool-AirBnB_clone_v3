#!/usr/bin/python3
"""
Amenities
"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """method that retrieves a list of all amenities"""
    all_amenities = storage.all('Amenity')
    amenities_list = all_amenities.values()
    amenities_json = []
    for amenity in amenities_list:
        amenities_json.append(amenity.to_dict())
    return jsonify(amenities_json)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """method that retrieves a state filter by id"""
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    return jsonify(my_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """method that deletes a amenity by id"""
    delete_amenity = storage.get('Amenity', amenity_id)
    if not delete_amenity:
        abort(404)
    else:
        delete_amenity.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """method to post a new amenity"""
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
    """method to update/put a amenity by id"""
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














#mi code

#!/usr/bin/python3
'''view for amenity'''

from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/amenities')
def get_amenities(amenity_id):
    '''Retrieves a list with all Amenity objects'''
    amenity = storage.get('Amenity', amenity_id)
    amenities_list = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods = ['GET'])
def get_amenity(amenity_id):
    '''Get amenity amenity object by id'''
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods = ['DELETE'])
def del_amenity(amenity_id):
    '''Delete amenity amenity object'''
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    else:
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    
     
@app_views.route('/amenities', methods = ['POST'])
def create_amenity(amenity_id):
    req = request.get_json()
    if req is None:
        abort(400, description='Not a JSON')
    if "name" not in req:
        abort(400, description='Missing name')
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    '''update amenity'''
    req = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    for key in req:
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(amenity, key, req[key])
    storage.save()
    return jsonify(amenity.to_dict()), 200
