from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_restful import Resource, Api, reqparse, fields , marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class usermodel(db.model):
        id = db.column(db.integer,primary_key=True)
         name =db.column(db.string(80), unique=True, nullable=False)
         email =db.column(db.string(80), unique=True, nullable=False) 

         def __repr__(self):
            return f"user(name = {self.name}, email ={self.name})"

        userFields = {
          'id':fields.integer,
         'name':fields.string,
         'email':fields.string,
          }

         user_args =reqparse.RequestParse()
         user_args.add argument('name', type=str, required=True,help="Name cannot be blank")
         user_args.add argument('email', type=str, required=True,help="email cannot be blank")

 class Users (Resource):
         @marshal_with(userFields)
         def get(self):
         users =UserModel.query.all()
         return users
                                                            
        @marshal_with(userFields)
                 def post (self):
                args =user_args.parse-args()
                user =usermodel(name=args["name"], email=args["email"])
                 db.session.add(user)
                 db.session.commit()
                users =usermodel.query.all()
                 return users, 201
                                                                                                                    
 class user(Resource): 
      @marshal_with(userFields)
         def get (self, id):
         user =usermodel.query.filter_by(id=id).first()
        if not user:
         abort (404, "user not found")
         return user
                                                                                                                                                                                                          

          @marshal_with(userFields)
          def patch (self, id):
         args =user_args.parse-args() 
        user =usermodel.query.filter_by(id=id).first()
   if not user:
         abort (404, "user not found")
           user.name =args ["name"]
         user.email =args["email"]
         db.session.commit()                                                                                                                                                                                                                                                                                                                                   
                 return user                                                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                                                    
  @marshal_with(userFields)
  def delete (self, id):
         user =usermodel.query.filter_by(id=id).first()
 if not user:
    abort (404, "user not found"t) 
    db.session.delete(user)
    db.session.commit 
users =usermodel.query.all()
         return users, 204
         api.add_resource(Users, '/api/users/')
         api.add_resource(User, '/api/users/<int:id>' \)
