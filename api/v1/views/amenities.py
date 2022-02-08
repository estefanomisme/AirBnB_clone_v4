#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """return all amenities"""
    amenities = [amenity.to_dict() for amenity in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_State(amenity_id):
    """amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        amenity = amenity.to_dict()
        return jsonify({amenity}), 200
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(amenity_id):
    """Delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        amenity.delete()
        storage.save()
        return jsonify({})
    return abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post():
    """Create a object"""
    if not request_json:
        return jsonify({"error": "Not a JSON"}), 404
    elif "name" not in request_json:
        return make_response(jsonify({"error": "Missing name"}), 404)
    jsn = request.get_json()
    obj = Amenity(**jsn)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put(amenity_id):
    """Update a amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    elif not request.get_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
