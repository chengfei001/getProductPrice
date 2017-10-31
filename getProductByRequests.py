from requests import  request
from json import dumps
import  sys
from PIL import Image
import pytesseract
from json import loads


# mongodb
from pymongo import MongoClient
client = MongoClient('localhost',27017)

# 链接mongodb
db = client.product_price
# connection = db.product
products = db.product
prices =db.price
# print(product.find_one())
# 链接mongodb


#获取图片#
#图片地址 字节流http://210.73.89.76/ServiceSelect/GetCode?t=150304757473'
response = request(method='get', url='http://210.73.89.76/ServiceSelect/GetCode?t=1503047574735')
f = open('vcode.jpg','wb')
f.write(response.content)
f.close()
# print(response.cookies.get('ASP.NET_SessionId'))
cookies = 'ASP.NET_SessionId='+ response.cookies.get('ASP.NET_SessionId')
#获取图片#


#获取验证码结果
im = Image.open('vcode.jpg')
im.convert('L')

validataCode = pytesseract.image_to_string(im)
code = validataCode
# print(code)

# code = input('验证码是什么？')
#获取验证码结果

#验证码验证#

# cookies = 'ASP.NET_SessionId=axpz1xspzfwk413riiy1yrp2'
headers = {'Content-Type':'application/json','Cookie':cookies}
data =  dumps({'InputCode':code})
response = request(method='post', url='http://210.73.89.76/ServiceSelect//RegInputCode', data=data, headers=headers)

#验证码验证#


#获取数据 产品信息
#获取数据链接  http://210.73.89.76/ServiceSelect/GetHosSelectList?page=1&pageSize=10

# headers = {'Cookie':cookies}
# pageNo = 1
# pageSize = 100
# response = request(method='post', url='http://210.73.89.76/ServiceSelect/GetHosSelectList?page=1&pageSize=1&InputCode=', headers=headers)
#
# total = loads(response.text)['Total']
# pageCount = total/pageSize
#
#
# while pageNo < pageCount+1:
#     response = request(method='post', url='http://210.73.89.76/ServiceSelect/GetHosSelectList?page='+str(pageNo)+'&pageSize='+str(pageSize)+'&InputCode=', headers=headers)
#     s =response.text
#     # print(s)
#     productData =  loads(s)['Data']
#     # print(isinstance(productData,list))
#     result = products.insert_many(productData)
#     pageNo = pageNo + 1
#     print(pageNo)


# print(str(loads(response.json())['Data']))

#获取数据



#从MongoDB中取出产品ID，再从网页获取价格及医院信息
# productsList = products.find()
productsList = products.find({'RN':{'$gt':6024}})
for product in productsList:
    #获取数据 医院和价格
    #链接 http://210.73.89.76/ServiceSelect/GridOrgInfoList
    #数据 page=1
    #    pageSize=100
    #    Id=DATA10000000000012822804
    print(product['RN'])
    data = {'page':'1', 'pageSize':'100', 'ProductId': product['ID'], 'InputCode':''}
    headers = {'Cookie':cookies}
    response = request(method='post', url='http://210.73.89.76/ServiceSelect/GridOrgInfoList', data= data, headers=headers)
    # print(product['RN'])

    priceJson = response.json()['Data']
    newPrice = []

    for price in priceJson:

        del price['RN']
        price['productId'] = product['ID']

        newPrice.append(price)

    print (newPrice)
    if len(newPrice):
        prices.insert_many(newPrice)
#获取数据 医院和价格