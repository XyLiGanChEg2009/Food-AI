from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import json
import logging
from model.test import get_keys as get_neru_answer

from api.DB import DB

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = DB()

def errorResponse(message:str , statusCode: int):
    app.logger.error(message)
    return jsonify({"status": "error", "message": message}), statusCode
    

@app.route("/get_products", methods=["GET"])
def get_products():
    query = request.args.get("query")
    if query is None or not query.strip() or not isinstance(query, str):
        return jsonify(db.get_products())
    else:
        if not isinstance(query, str):
            return errorResponse("request should be str", 400)
         
        userRequest = query.strip()
        keys = get_neru_answer(userRequest)
        
        if not keys:
            return errorResponse("Neuro doesnt answer", 500)
    
        return jsonify(db.get_products_by_keys(keys))

@app.route("/get_product_by_id", methods=["GET"])
def get_product_by_id():
    prodId = request.args.get("id")
    
    if prodId is None:
        return errorResponse("Id is none", 400)
    
    if not isinstance(id, int):
        return errorResponse("Id type should be int", 400)
    
    product = jsonify(db.get_product_by_id(prodId))
    return product

@app.route("/get_restaurants", methods=["GET"])
def get_restaurants():
    restId = request.args.get("id")
    if restId is None:
        return jsonify(db.get_restaurants())
    else:
        try:
            restId = int(restId)
        except ValueError:
            return errorResponse("Id should be an integer", 400)
        if restId <= 0:
            return errorResponse("Id should be a positive number", 400)
        
        return jsonify(db.get_restaurants(restId))

@app.route("/add_product", methods=["POST"])
def add_product():
    try:
        prod = request.get_json()
        app.logger.debug(f"Recived JSON data: {prod}")
        
        if not isinstance(prod, dict):
            return errorResponse("Invalid json format recived", 400)
        
        name, img_src, price, weight, keys, restaurant_id = (prod["name"], prod["img_src"], prod["price"], prod["weight"], prod["keys"], prod["restaurant_id"])    
        
        if not (isinstance(name, str) and isinstance(img_src, str)):
            return errorResponse("Name and img_src must be strings", 400)
        if not (isinstance(price, int) and isinstance(weight, int) and isinstance(restaurant_id, int)):
            return errorResponse("Price, weight and restaurant_id must be integers", 400)
        if not (name.strip() and img_src.strip()): 
            return errorResponse("Name and img_src cannot be empty", 400)
        if not (price > 0 and weight > 0 and restaurant_id >= 0): 
            return errorResponse("Price and weight must be positive, restaurant_id must be non-negative", 400)
        
        result = db.add_product(img_src, price, weight, name, restaurant_id, keys)
        
        if result["status"] == "ok":
          return jsonify({"status": "ok", "message": "Product added successfully"}), 200 
        else:
          app.logger.error("Failed to add product to the database")
          return jsonify({"status": "error", "message": f"{result['message']}"}), 500
       
    except json.JSONDecodeError:
        return errorResponse("Invalid JSON format received", 400)

@app.route("/add_restaurant", methods=["POST"])
def add_restaurant():
    try:
        prod = request.get_json()
        app.logger.debug(f"Recived JSON data: {prod}")
        
        if not isinstance(prod, dict):
            return errorResponse("Invalid json format recived", 400)
        name = prod["name"]
        
        if not isinstance(name, str):
            return errorResponse("Name must be strings", 400)
        
        if not name.strip():
            return errorResponse("Arguments are empty or null", 400)
        
        result = db.add_restaurants(name)
        
        if result["status"] == "ok":
          return jsonify({"status": "ok", "message": "Restaurant added successfully"}), 200 
        else:
          app.logger.error("Failed to add restaraunt to the database")
          return jsonify({"status": "error", "message": f"{result['message']}"}), 500
       
    except json.JSONDecodeError:
        return errorResponse("Invalid JSON format received", 400)
    

# @app.route("/add_product", methods=["put"])
# def update_product_by_id(id):
#     prod = request.get_json()
#     name = prod["name"]
#     img_src = prod["img_src"]
#     price = prod["price"]
#     weight = prod["weight"]
#     if prod == 415 or prod == 400:
#         return 510
#     elif name == "" or img_src == "" or price != price or weight != weight:
#         return "Arguments are empty or null", 400
#     else:
#         result = db.update_product(id, img_src, price, weight, name)
#         return result