#!/usr/bin/python3
'''view for amenity'''

from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/amenities')
def get_amenities():
    '''Retrieves a list with all Amenity objects'''
    amenities = storage.all('Amenity')
    amenities_list = []
    for amenity in amenities.values:
        amenity_list-append(amenity)
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    '''Get amenity amenity object'''
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
    '''New amenity'''
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
        abort(400, description='Not a JSON')
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
