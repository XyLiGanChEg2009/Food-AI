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


@app.route("/get_products", methods=["GET"])
def get_products():
    query = request.args.get("query")
    if query is None or query == "" or not isinstance(query, str):
        return jsonify(db.get_products())
    else:
        if not query:
            app.logger.error("request is empty")
            return jsonify({"status": "error", "message": "request is empty"})
        
        if not isinstance(query, str):
            app.logger.error("request should be str")
            return jsonify({"status": "error", "message": "request should be str"})
         
        userRequest = query.strip()
        keys = get_neru_answer(userRequest)
        
        if not keys:
            app.logger.error("Neuro doesnt answer")
            return jsonify({"status": "error", "message": "Neuro doesnt answer"})
         
        response = db.get_products_by_keys(keys)
        return jsonify(response)

@app.route("/get_product_by_id", methods=["GET"])
def get_product_by_id():
    #query = request.args.get("query")
    prodId = request.args.get("id")
    
    if id is None:
        app.logger.error("Id is none")
        return jsonify({"status": "error", "message": "id is none"}), 400
    
    if not isinstance(id, int):
        app.logger.error("Id type should be int")
        return jsonify({"status": "error", "message": "Id type should be int"}), 400
    
    product = jsonify(db.get_product_by_id(prodId))
    return product

@app.route("/add_product", methods=["POST"])
def add_product():
    try:
        prod = request.get_json()
        app.logger.debug(f"Recived JSON data: {prod}")
        
        if not isinstance(prod, dict):
            app.logger.error("Invalid json format recived")
            return jsonify({"status": "error", "message": "Invalid json format"}), 400
        name = prod["name"]
        img_src = prod["img_src"]
        price = prod["price"]
        weight = prod["weight"]
        keys = prod["keys"]
        
        if any(item is None for item in [name, img_src, price, weight]):
            app.logger.error("Missing required arguments")
            return jsonify({"status": "error", "message": "Missing required arguments"}), 400
        
        if not all(isinstance(item, str) for item in [name, img_src]):
            app.logger.error("Name and img_src must be strings")
            return jsonify({"status": "error", "message": "Name and img_src must be strings"}), 400
        
        if not isinstance(price, int) or not isinstance(weight, int):
            app.logger.error("Price and weight must be int")
            return jsonify({"status": "error", "message": "Price and weight must be int"}), 400
        
        if not all([name.strip(), img_src.strip()]):
            app.logger.error("Arguments are empty or null")
            return jsonify({"status": "error", "message": "Arguments are empty or null"}), 400
        
        if price <= 0 or weight <= 0:
          app.logger.warning("Price and weight must be positive values")
          return jsonify({"status": "error", "message": "Price and weight must be positive values"}), 400
        
        result = db.add_product(img_src, price, weight, name, keys)
        
        if result["status"] == "ok":
          return jsonify({"status": "ok", "message": "Product added successfully"}), 200 
        else:
          app.logger.error("Failed to add product to the database")
          return jsonify({"status": "error", "message": f"{result["message"]}"}), 500
       
    except json.JSONDecodeError:
        app.logger.warning("Invalid JSON format received")
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

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