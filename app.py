from flask import Flask, render_template, request
# from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://aniket:CollegePlace107@cluster0.8opd5.mongodb.net/?retryWrites=true&w=majority")

# db = client.test

# mongo = PyMongo(app)
# db = mongo.db

db = client["users"]
collection = db["userdata"]
add_user_collection = db["new_users"]

food = client["food"]
print(food)

# print(food_collection)


@app.route("/")
def index():
    
    return render_template("index.html")

@app.route('/hotel',methods=['post'])
def hotel():
    msg = "Wrong email or password"
    ans = []
    if request.method == "POST":
        email = request.form['email']
        entered_password = request.form['password']
        
        item = add_user_collection.find({"email":email})
        for i in item:
            if i['org'] == 'Hotel':
                if i['password'] == entered_password:
                    idx = list(food.hotelngo.find({"hid":i['_id']}))
                    if len(idx)>=1:
                        requested_food = list(food.food_data.find({"_id":idx[0]['fid']}))
                         
                         
                        print(idx)
                        print(requested_food)
                        if requested_food:    

                            return render_template("hotel.html", requested_food=requested_food)
                    else:
                        return render_template("hotel.html")
            if i['org'] == 'ngo':
                if i['password'] == entered_password:
                    food_data = list(food.food_data.find())
                    return render_template('ngo.html',food_data=food_data)
            else:
                return render_template("index.html",msg = msg)
      

@app.route('/requested',methods=['POST'])
def requested():
    button_counter = request.form['buttonCounter']
    print(button_counter)
    food_data = list(food.food_data.find())
    req = food_data[int(button_counter) - 1]

    item = add_user_collection.find({"name":req['name']})
    item = item[0]
    food.hotelngo.insert_one({'fid':req['_id'],'hid':item['_id']})
    
    return "Request Sent! "
      
@app.route('/register',methods=['post'])
def register():
    return render_template("register.html")

# @app.route('/update-counter', methods=['POST'])
# def update_counter():
#     button_counter = request.form['buttonCounter']
#     print(button_counter)
#     # Do something with the button_counter value
#     return 'Button counter received successfully!'


@app.route('/addUser',methods=['post'])
def addUser():
    
    # hotel name
    # phone
    # email
    # pass 
    # location
    
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        email = request.form['email']
        org = request.form['org']
        password = request.form['password']
        add = {"name":name, "address":address,"contact":contact,"email":email,"org":org, "password":password}
        
        add_user_collection.insert_one(add)
    
    
    return render_template("index.html")


if __name__ == '__main__':
   app.run(debug=True)


# from flask import Flask
# from flask_pymongo import PyMongo

# app = Flask(__name__)

# app.config['MONGO_URI'] = 'mongodb+srv://aniket:<password>@cluster0.8opd5.mongodb.net/?retryWrites=true&w=majority'

# mongo = PyMongo(app)

# @app.route('/')
# def index():
    # user_collection = mongo.db.users
    # users = user_collection.find({})
#     return str(users)

# if __name__ == '__main__':
#     app.run()
