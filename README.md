**Documentation**

User authentication and authorizationimplementation.

**TechStack**

Backend (Python)

Database (PostgreSQL)

Flask

Jwt

**ProjectStructure**

/SMTMINTERN/Task5/

jwt-auth-flask/

│── flask\_app/

│   │── \_\_init\_\_.py

│   │── models.py

│   │── routes.py

│   │  │── config.py

│── migrations/

│── .gitignore       # (Ignore .venv and other unnecessaryfiles)

│── app.py      # (Main entry point) 

│── db.py

│── hash.py       # (Convert plain text password to hashfor db.)

│── README.md        # (Project documentation)




**Step-By-StepImplementation**

1.    Create your models in models.py

fromflask\_login import UserMixin

fromflask\_app import db

importbcrypt

classUser(db.Model, UserMixin):

    \_\_tablename\_\_ = "users"

    id = db.Column(db.Integer,primary\_key=True)

    username = db.Column(db.String(50),unique=True, nullable=False)

    full\_name = db.Column(db.String(100),nullable=False)

    email = db.Column(db.String(100),unique=True, nullable=False)

    hashed\_password = db.Column(db.String(255),nullable=False)  # Store hashed passwords

    role = db.Column(db.String(10),nullable=False) 

    def set\_password(self, password):

        """Hashes the passwordbefore storing it."""

        self.hashed\_password =bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check\_password(self, password):

        """Verifies the passwordagainst the stored hash."""

        returnbcrypt.checkpw(password.encode('utf-8'), self.hashed\_password.encode('utf-8'))

    def \_\_repr\_\_(self):

        return f""

fromflask\_app import db

classProduct(db.Model):

    id = db.Column(db.Integer,primary\_key=True, autoincrement=True) #Ensures auto-increment in id

    name = db.Column(db.String(100),nullable=False)

    price = db.Column(db.Float, nullable=False)


    

2.     _Initializeimports for app in \_\_init\_\_.py_

fromflask import Flask

fromflask\_sqlalchemy import SQLAlchemy

fromflask\_jwt\_extended import JWTManager

fromflask\_login import LoginManager

fromflask\_app.config import Config

fromflask\_bcrypt import Bcrypt

fromflask\_migrate import Migrate

db= SQLAlchemy()

bcrypt= Bcrypt()

jwt= JWTManager()

login\_manager= LoginManager()

defcreate\_app():

    app = Flask(\_\_name\_\_)

    app.config.from\_object(Config)

    # Initialize extensions

    bcrypt.init\_app(app)

    db.init\_app(app)

    Migrate(app, db)

    jwt.init\_app(app)

    login\_manager.init\_app(app)

    with app.app\_context():

        db.create\_all()

    from flask\_app.routes import auth\_bp,product\_bp

    app.register\_blueprint(auth\_bp)

    app.register\_blueprint(product\_bp)

                           return app


                           

3.     _Createyour apps to run routes in app.py_

fromflask import Flask

fromflask\_app import create\_app

app= create\_app()

if\_\_name\_\_ == '\_\_main\_\_':

    app.run(debug=True)


    

4.     _Createconfigurations in config.py_

classConfig:

    SQLALCHEMY\_DATABASE\_URI ='postgresql://postgres:Alish@123@localhost/Intern'

    SQLALCHEMY\_TRACK\_MODIFICATIONS = False

    SECRET\_KEY ='5791628bb0b13ce0c676dfde280ba245'

    JWT\_SECRET\_KEY ='5791628bb0b13ce0c676dfde280ba245'

    JWT\_TOKEN\_LOCATION = \['headers'\]

    JWT\_HEADER\_NAME = 'Authorization' 

    JWT\_HEADER\_TYPE = 'Bearer'

    JWT\_ACCESS\_TOKEN\_EXPIRES = 3600

    Debug = True


    

5.     _CreateRoutes in routes.py for admin and user for GET and POST request_

from flask import Blueprint,request, jsonify, current\_app

from flask\_login importlogin\_user, current\_user, logout\_user, login\_required

from flask\_jwt\_extended importcreate\_access\_token, jwt\_required, get\_jwt\_identity, get\_jwt

from flask\_app.models importUser, Product

from flask\_app import db, bcrypt

from functools import wraps

auth\_bp = Blueprint('auth\_bp',\_\_name\_\_)   

product\_bp =Blueprint('product\_bp', \_\_name\_\_)

\# Fetch Users (for testing)

@auth\_bp.route("/test-users",methods=\["GET"\])

def get\_users():

    try:

        users = User.query.all()

        user\_list = \[{"id": user.id,"username": user.username, "email": user.email} for user inusers\]

        return jsonify({"users":user\_list}), 200

    except Exception as e:

        return jsonify({"error":str(e)}), 500

# Login Route

@auth\_bp.route('/login',methods=\['POST'\])

def login():

    try:

        data = request.json

        with current\_app.app\_context(): 

            user = User.query.filter\_by(username=data\['username'\]).first()

        if user andbcrypt.check\_password\_hash(user.hashed\_password, data\['password'\]):

            access\_token =create\_access\_token(identity=str(user.id), additional\_claims={"role":user.role})

            returnjsonify({"message": "Login successful!","access\_token": access\_token})

        return jsonify({"message":"Invalid username or password"}), 401

    except Exception as e:

        print(f"❌ ERROR: {str(e)}") 

        return jsonify({"error":str(e)}), 500

def admin\_required(fn):

    @wraps(fn)

    @jwt\_required()

    def wrapper(\*args, \*\*kwargs):

        try:

            role =get\_jwt().get("role")  #Extract role from JWT claims

            if role != "admin":

                return jsonify({"message":"Admin access required"}), 403

            return fn(\*args, \*\*kwargs)

        except Exception as e:

            return jsonify({"error":str(e)}), 500

    return wrapper

#Fetch Products (User &Admin)

@product\_bp.route('/products', methods=\['GET'\])

@jwt\_required()

def get\_products():

    try:

        products = Product.query.all()

        return jsonify(\[{"id": p.id,"name": p.name, "price": p.price} for p in products\]), 200

    except Exception as e:

        return jsonify({"error": str(e)}),500

@product\_bp.route('/products',methods=\['POST'\])

@admin\_required

def add\_product():

    try:

        data = request.get\_json()

        if not data or "name" not indata or "price" not in data:

            returnjsonify({"message": "Product name and price arerequired"}), 400

        new\_product =Product(name=data\['name'\], price=data\['price'\]) 

        db.session.add(new\_product)

        db.session.commit()

        return jsonify({"message":"Product added successfully!", "product\_id":new\_product.id}), 201

    except Exception as e:

        return jsonify({"error":str(e)}), 500

\# Update Product (Admin Only)

@product\_bp.route('/products/',methods=\['PUT'\])

@admin\_required

def update\_product(product\_id):

   try:

        data = request.get\_json()

        product =Product.query.get\_or\_404(product\_id)

        product.name = data.get('name',product.name)

        product.price = data.get('price',product.price)

        db.session.commit()

        return jsonify({"message":"Product updated successfully!"}), 200

    except Exception as e:

        return jsonify({"error":str(e)}), 500

\# Delete Product (Admin Only)

@product\_bp.route('/products/',methods=\['DELETE'\])

@admin\_required

def delete\_product(product\_id):

    try:

        product =Product.query.get\_or\_404(product\_id)

        db.session.delete(product)

        db.session.commit()

        return jsonify({"message":"Product deleted successfully!"}), 200

    except Exception as e:

        return jsonify({"error":str(e)}), 500

\# Default Route

@auth\_bp.route('/',methods=\['GET'\])

def home():

    return jsonify({"message":"Welcome to the Flask API!"}), 200   

**Run theProject**

·      .venv\\Scripts\\activate

·      Runserverusing flask run

**For admin**

SendPOST request at [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login) with JSON body {

  "username": "Juniper",

  "password": "xxxx"

}

Accesstoken is granted.put that access token in authentication header for products POST request with key: Authorization and Value: BearereyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczOTk3NDk2MSwianRpIjoiYTdkOTkyNWMtNjkyNy00MzY2LWIwMzYtMTcxYzkyZjFlM2RhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3Mzk5NzQ5NjEsImNzcmYiOiJiZTRmOGQyZC04Y2IzLTRiOTMtYTMwYi01YTA2ZDJmNzhhN2EiLCJleHAiOjE3Mzk5Nzg1NjEsInJvbGUiOiJhZG1pbiJ9.2d52S60zKfuuvpRbdWoVADsKDtCvI6QajcLf811xmXY

Toadd products

SendPOST request at [http://127.0.0.1:5000/products](http://127.0.0.1:5000/products) with json body {

  "name": "CBR",

  "price": "50"

}

**AdminLogin**

**SendingPOST request for** [**http://127.0.0.1:5000/login**](http://127.0.0.1:5000/login)
![Image](https://github.com/user-attachments/assets/f88ec9a4-cd19-406b-9851-fcce6396daed)

**SendingPOST request for** [http://127.0.0.1:5000/products](http://127.0.0.1:5000/products)
![Image](https://github.com/user-attachments/assets/b8ae0bcb-9546-4643-bd3c-ab222ff09bb9)

**UserLogin**

**Send POSTrequest at** [**http://127.0.0.1:5000/login**](http://127.0.0.1:5000/login)
![Image](https://github.com/user-attachments/assets/142a0206-7ed9-4a7e-bd25-030c21db541b)

**AddingProducts by User**
![Image](https://github.com/user-attachments/assets/734ea2fc-f771-42a1-bb79-59f1853566b9)

**Changesin the DatabaseUsers Table**
**UsersTable**
![Image](https://github.com/user-attachments/assets/b3c20bfc-5ab8-412d-81fe-e8ed3363a3ba)

**ProductsTable**
![Image](https://github.com/user-attachments/assets/929e70bb-b034-4172-b761-b29622cd3c1d)

**Conclusion:**

ThisFlask-jwt-authentication helps in authenticating and authorizing user using jwttokens.
