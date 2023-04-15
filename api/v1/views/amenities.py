
#!/usr/bin/python3
'''view for amenity'''

from flask import Flask, jsonify, request, abort
from models import storage
from console import classes
from api.v1.views import app_views

@app_views.route('/amenities')
def get_amenities():
    '''Retrieves a list with all Amenity objects'''
    amenity = storage.all('Amenity')
    amenities_list = []
    for obj in amenity.values():
        amenities_list.append(obj.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods = ['GET'])
def get_amenity(amenity_id):
    '''Get amenity amenity object by id'''
    amenity = storage.get(classes['Amenity'], amenity_id)
    if amenity is None:
        abort('404')
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods = ['DELETE'])
def del_amenity(amenity_id):
    '''Delete amenity amenity object'''
    amenity = storage.get(classes['Amenity'], amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
    
     
@app_views.route('/amenities', methods = ['POST'])
def create_amenity():
    req = request.get_json()
    if type(req) is not dict:
        abort('404', description= 'Not a JSON')
    if "name" in req:
        new_amenity = classes["Amenity"](**req)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 200
    else:
        abort(400, description= 'Missing name')


@app_views.route('amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """
    Update an Amenity amenity object
    """
    amenity = storage.get(classes["Amenity"], amenity_id)
    if amenity is None:
        abort('404')
    amenity = request.get_json()
    if type(amenity) is not dict:
        abort(400, description= 'Not a JSON')
    for key, value in amenity.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(amenity, key, value)
    storage.save()
    
    return jsonify(amenity.to_dict()), 200
