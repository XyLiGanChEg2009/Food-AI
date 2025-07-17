from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import json
import logging

from DB import DB

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

DATABASE = "../DB/foodAiDataBase.db"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = DB()

products = [
    {"img_src": "https://eda.yandex/images/15441079/0d09e9b391b58f23108d7de91f43de26-216x188.jpeg", "price": 10, "weight": 200, "name": "Samara vibes", "keys": ["основое_блюдо"]},
    {"img_src": "https://eda.yandex/images/15441079/3345f731bd1de2b3c1fe415a6e4b56fd-216x188.jpeg", "price": 30, "weight": 400, "name": "Kalach ua"},
    {"img_src": "https://eda.yandex/images/15252145/2e3595fabe130f69f1a70deb6df113f2-216x188.jpeg", "price": 5, "weight": 300, "name": "Igor starter pack"},
    {"img_src": "https://eda.yandex/images/3508859/113d03704c034c41740d6d181acc4c33-216x188.jpeg", "price": 6, "weight": 220, "name": "Гомик"},
    {"img_src": "https://eda.yandex/images/3806315/14a9f708fa28757cbee9daee95178a49-216x188.jpeg", "price": 4, "weight": 150, "name": "Baby sasuke"},
    {"img_src": "https://eda.yandex/images/1365461/e18ed97b0f1fd6a9aa358efb82c7e359-216x188.jpeg", "price": 8, "weight": 230, "name": "Marim"},
    {"img_src": "https://eda.yandex/images/3806466/4a5f726c1c2a1c79953d53482cfc329a-216x188.jpeg", "price": 12, "weight": 200, "name": "Maksim Kozlovskiyu"},
    {"img_src": "https://eda.yandex/images/3435765/802936e8fd5880aff83ffe130933bdd0-216x188.jpeg", "price": 43, "weight": 120, "name": "Вульпа"},
    {"img_src": "https://avatars.mds.yandex.net/i?id=b8fb85bdd1fef93630b9356abb3814e2_l-4753661-images-thumbs&n=13", "price": 120, "weight": 45000, "name": "standoff boost"},
    {"img_src": "https://eda.yandex/images/16473711/3c86e183f36b4b3cadb0bf7caedba405-216x188.jpeg", "price": 13, "weight": 300, "name": "Сайонара бой"},
    {"img_src": "https://avatars.mds.yandex.net/i?id=1e68a66a71909a4a051c8cac8d4bd3cd_l-5171568-images-thumbs&n=13", "price": 220, "weight": 220, "name": "Космо папа"},
]


@app.route("/get_products", methods=["GET"])
def get_products():
    #query = request.args.get("query")
    response = app.response_class(
        response=json.dumps(db.get_products()),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/get_product_by_id", methods=["GET"])
def get_product_by_id():
    #query = request.args.get("query")
    prodId = request.args.get("id")
    
    if id is None:
        app.logger.error("Id is none")
        return jsonify({"error": "id is none"}), 400
    
    if not isinstance(id, int):
        app.logger.error("Id type should be int")
        return jsonify({"error": "Id type should be int"}), 400
    
    print("xuy")
    response = app.response_class(
        response=json.dumps(db.get_product_by_id(prodId)),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/add_product", methods=["POST"])
def add_product():
    try:
        prod = request.get_json()
        app.logger.debug(f"Recived JSON data: {prod}")
        
        if not isinstance(prod, dict):
            app.logger.error("Invalid json format recived")
            return jsonify({"error": "Invalid json format"}), 400
        name = prod["name"]
        img_src = prod["img_src"]
        price = prod["price"]
        weight = prod["weight"]
        
        if any(item is None for item in [name, img_src, price, weight]):
            app.logger.error("Missing required arguments")
            return jsonify({"error": "Missing required arguments"}), 400
        
        if not all(isinstance(item, str) for item in [name, img_src]):
            app.logger.error("Name and img_src must be strings")
            return jsonify({"error": "Name and img_src must be strings"}), 400
        
        if not isinstance(price, int) or not isinstance(weight, int):
            app.logger.error("Price and weight must be int")
            return jsonify({"error": "Price and weight must be int"}), 400
        
        if not all([name.strip(), img_src.strip()]):
            app.logger.error("Arguments are empty or null")
            return jsonify({"error": "Arguments are empty or null"}), 400
        
        if price <= 0 or weight <= 0:
          app.logger.warning("Price and weight must be positive values")
          return jsonify({"error": "Price and weight must be positive values"}), 400
        
        result = db.add_product(img_src, price, weight, name)
        
        if result["status"] == "ok":
          return jsonify({"message": "Product added successfully"}), 200 
        else:
          app.logger.error("Failed to add product to the database")
          return jsonify({"error": "Failed to add product"}), 500
       
    except json.JSONDecodeError:
        app.logger.warning("Invalid JSON format received")
        return jsonify({"error": "Invalid JSON format"}), 400

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