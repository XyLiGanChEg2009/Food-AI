from flask import Flask
from flask_cors import CORS
from flask import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route("/get_products")
def get_products():
    #query = request.args.get("query")
    response = app.response_class(
        response=json.dumps(products),
        status=200,
        mimetype='application/json'
    )
    return response
