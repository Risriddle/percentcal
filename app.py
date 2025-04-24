from flask_restful import Resource, Api
from flask import render_template
from os import system
from flask import *
import pymongo 

client = pymongo.MongoClient("mongodb+srv://kanojo:kanojo@cluster0.0pien5l.mongodb.net/?retryWrites=true&w=majority")
print(client)

#Creating a collection/datafield
db = client["percent"]  #name of DB
collection = db["data"] # name of collection
print(client)

system("clear")

#staring web app
app = Flask(__name__)
api = Api(app)

#home page
class Home(Resource):
  def get(self):
    return make_response(render_template('home.html')) 
  def post(self):
    return make_response(render_template('home.html')) 
    



#registration page
class Register(Resource):
  def get(self):
    return make_response(render_template('register.html'))  

  def post(self):
    return make_response(render_template('register.html'))   

#Login page
class Login(Resource):
  def get(self):

    return make_response(render_template('login.html'))  

  def post(self):
    name = request.form.get('name') # for post method
    age = request.form.get('age')
    dob= request.form.get('dob')
    pwd = request.form.get('pwd')
    email = request.form.get('email')
    school = request.form.get('school')
    board = request.form.get('board')

    dict = {"name":name,"email":email,"pass":pwd,"age":age,"dob":dob,"school":school,"board":board}
    collection.insert_one(dict)
    print("-------------------------------")
    print("Data store to db")
    return make_response(render_template('login.html')) 

# after login welcome page
class Welcome(Resource):
  def get(self):
    return make_response(render_template('register.html'))

  def post(self):
    print('==============================================================================================')
    pwd = request.form.get('pass')
    mail = request.form.get('email')
    data = collection.find_one({"email":mail,"pass":pwd},{"_id":0})
    print("-------------------------------")
    if data != None and mail == data['email'] and pwd == data['pass']:
      print(" Login done --------------------------------")
      print(data)
      return make_response(render_template('welcome.html',name=data['name'],age=data['age'],dob=data['dob'],school=data['school'],board=data['board']))
    else:
      print("wrong pass")
      return "invalid email or password"      
      return make_response(render_template('login.html')) 

#calculate percentage page  
class Calculate(Resource):  
  def get(self):
    return make_response(render_template('home.html'))  
  def post(self):
    eng = request.form.get('eng')
    math = request.form.get('math')
    sci = request.form.get('sci')
    oops = request.form.get('oops')
    de = request.form.get('de')
    percent= ((int(eng)+int(math)+int(de)+int(oops)+int(sci))/500)*100
    return make_response(render_template('calculate.html',percent=percent))
    def exit():
        return make_response(render_template('welcome.html'))
    def home():
        return make_response(render_template('home.html')) 
    



api.add_resource(Home, '/',methods=['GET','POST'])  
api.add_resource(Login, '/login',methods=['GET', 'POST'])
api.add_resource(Welcome, '/welcome',methods=['GET', 'POST'])
api.add_resource(Register, '/register',methods=['GET', 'POST'])
api.add_resource(Calculate, '/calculate',methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=False)   