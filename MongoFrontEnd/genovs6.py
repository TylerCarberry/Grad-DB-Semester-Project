from flask import Flask,render_template,url_for,request,flash,redirect
import os
import urllib
import datetime
import dateutil.relativedelta
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://34.202.12.241:27017/carberryt9"
mongo = PyMongo(app)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('/home.html')

@app.route('/customer/')
def customer():
    return render_template('/customer.html')

@app.route('/customers/<specify>/')
def customers(specify):
    if specify=="rowan":
        customers = mongo.db.customers.find({"source":"rowan"})
    elif specify=="others":
        customers = mongo.db.customers.find({"source":{"$nin":["rowan"]}})
    elif specify=="notActive":
		d = datetime.datetime.now()
		d2 = d - dateutil.relativedelta.relativedelta(months=1)
		customers = mongo.db.customers.find({"Last_Active":{"$lte":d2}})
    return render_template('/customers.html',customers = customers)

@app.route('/product/')
def product():
    return render_template('/product.html')

@app.route('/products/<specify>/')
def products(specify):
    if specify=="rowan":
		products = mongo.db.products.find({"source":"rowan"})
    elif specify=="others":
		products = mongo.db.products.find({"source":{"$nin":["rowan"]}})
    elif specify=="notWell":
		d = datetime.datetime.now()
		d2 = d - dateutil.relativedelta.relativedelta(months=1)
		products = mongo.db.products.find({"Last_Bought":{"$lte":d2}})
    elif specify=="bellowMinimum":
		products = mongo.db.products.find({"Num_In_Stock":{"$lte":10}})
    elif specify=="restock":
		products = mongo.db.restock.find()
		return render_template('/restock.html',products = products)
    return render_template('/products.html',products = products)

if __name__ == "__main__":
	app.run()
