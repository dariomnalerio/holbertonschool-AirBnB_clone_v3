#!/usr/bin/python3
''' Endpoints for Amenity objects '''

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from console import classes


@app_views.route('/amenities')
def get_all_amenities():
    """Return the list of all amenities."""
    amenities = [amenity.to_dict()
                 for amenity in storage.all(classes["Amenity"]).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    """ Retrieves a Amenity object """
    amenities = storage.all(classes["Amenity"])
    if f"Amenity.{amenity_id}" in amenities:
        return jsonify(amenities[f"Amenity.{amenity_id}"].to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get(classes['Amenity'], amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """Create a new amenity."""
    try:
        req = request.get_json()
        if not req:
            abort(400, description="Not a JSON")
        if "name" not in req:
            abort(400, description="Missing name")
        amenity_instance = classes["Amenity"](**req)
        storage.new(amenity_instance)
        storage.save()
        return amenity_instance.to_dict(), 201
    except Exception:
        abort(400, description="Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get(classes['Amenity'], amenity_id)
    if amenity:
        try:
            req = request.get_json()
            if not req:
                abort(400, description="Not a JSON")
            for key, value in req.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)
            storage.save()
            return jsonify(amenity.to_dict()), 200
        except Exception:
            abort(400, description="Not a JSON")
    else:
        abort(404)
