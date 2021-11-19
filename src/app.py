"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    # this is how you can use the Family datastructure by calling its methods
    response_body = jackson_family.get_all_members()
    return jsonify(response_body), 200

#POST new family members
@app.route('/member', methods=['POST'])
def post_members():
    body = request.get_json()
    if body is None:
        return jsonify({"message":"The request body is null"}),400
    elif 'first_name' not in body:
        return jsonify({"message":"You need to specify the name"}),400
    elif 'age' not in body:
        return jsonify({"message":"You need to specify the age"}),400
    elif 'lucky_numbers' not in body:
        return jsonify({"message":"You need to specify a lucky_numbers list"}),400
    elif not isinstance(body.get("age"), int):
        return jsonify({"message":"Age must be a integer number greather than 0"}),400
    else:
        if 'id' in body:
            member = jackson_family.get_member(body.get("id"))
            if member:
                return jsonify({"message":"ID already exists"}),400

        new_member = jackson_family.add_member({
            "id":body.get("id"),
            "first_name":body.get("first_name"),
            "age":body.get("age"),
            "lucky_numbers":body.get("lucky_numbers")
        })
        return jsonify({"message":f"{new_member.get('id')} added ok"}), 200

#GET, PUT, DELETE members of family
@app.route('/member/<int:member_id>', methods=['GET','DELETE','PUT'])
def manage_members(member_id):

    member = jackson_family.get_member(member_id)

    if request.method == 'PUT': #UPDATE
        if not member:
            return jsonify({"message":"error: ID not exists"}), 404
        body = request.get_json()    
        if body is None:
            return jsonify({"message":"The request body is null"}),400
        elif 'age' in body and (not isinstance(body.get("age"), int)):
            return jsonify({"message":"Age must be a integer number greather than 0"}),400
        else:
            new_member = jackson_family.update_member(member_id,{
                "first_name":body.get("first_name"),
                "age":body.get("age"),
                "lucky_numbers":body.get("lucky_numbers")
            })
            return jsonify({"message":f"{member_id} updated ok"}), 200

    elif request.method == "DELETE": #DELETE
        if member is None:
            return jsonify({"message":"error: ID not exists"}),404
        else:
            jackson_family.delete_member(member_id)
            return jsonify({"done":True, "message":f"{member_id} deleted ok"}), 200

    else: #GET
        if member is None:
            return jsonify({"message":"error: ID not exists"}),404
        else:
            return jsonify(member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
