from flask import Flask
from flask import abort
from json import dumps
from pymongo import MongoClient
from flask import jsonify



client = MongoClient('localhost',27017)

# 链接mongodb
db = client.product_price
products = db.product
prices = db.price


app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
def index():
    return '<h1>first web</h1>'

@app.route('/search/<keyWord>')
def returnProductInfo(keyWord):
    if keyWord :
        productJson = [doc for doc in products.find({'NAME_CHN':{'$regex':keyWord}},{'_id':0}) ]
        datatext = dumps(productJson, ensure_ascii=False)
        datatext2 = datatext[1:-2]

        return jsonify({"data":productJson})
    else:
        return abort(404)


@app.route('/findPriceBy/<productId>')
def findPriceByProductId(productId):
    if productId:
        pricesJson = [doc for doc in prices.find({'productId':productId},{'_id':0})]

        return dumps(pricesJson, ensure_ascii=False)
    else:
        return  abort(404)

if __name__ == '__main__':
    app.run(debug=True)