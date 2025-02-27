import hashlib
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from pathlib import Path
from bson import ObjectId
import jwt
from datetime import datetime, timedelta


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'nongtonklasudnaruk'
MONGO_URI = "mongodb+srv://67011392:ceiyingyai@cluster0.3tqmk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.get_database("mydb")

class Auth:
    def __init__(self):
        self.__SECRET_KEY = SECRET_KEY

    def signin(self, email, password):
        collection = db.get_collection("user")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = collection.find_one({"email": email, "password": password_hash})
        if user:
            token = jwt.encode(
                {"email": email, "exp": datetime.utcnow() + timedelta(hours=24)}, 
                SECRET_KEY, 
                algorithm="HS256"
            )
            response = Response({"message": "Login successful", "token": token}, status=status.HTTP_200_OK)
            return response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def signup(self, payload):
        collection = db.get_collection("user")
        email = payload.email
        name = payload.name
        password = payload.password
        phone = payload.phone
        address = payload.address
        id = payload.id
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = collection.find_one({"email": email})
        if user:
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        new_user = {
            "name": name,
            "email": email,
            "password": password_hash,
            "phone": phone,
            "address": address,
            "id": id,
            "Inventory": [],
            "Transaction": [],
            "type": "user"
        }
        collection.insert_one(new_user)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class InventoryManager:
    def __init__(self):
        self.__inventory = []

    def add_item(self, item, quantity):
        pass

class Transaction:
    def __init__(self):
        self.__balance = 0
        self.__transactions = []

    def add_transaction(self, transaction):
        pass

class User:
    def __init__(self, id, name, email, password, phone, address):
        self.__id = id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__phone = phone
        self.__address = address
        self.__transaction = Transaction()
        self.__inventory = InventoryManager()
        self.__type = "user"

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def phone(self):
        return self.__phone

    @property
    def address(self):
        return self.__address

    @property
    def transaction(self):
        return self.__transaction

    @property
    def inventory(self):
        return self.__inventory

    @property
    def type(self):
        return self.__type
    @property
    def password(self):
        return self.__password

class Retail(User):
    def __init__(self, id, name, email, password, phone, address, shop_name):
        super().__init__(id, name, email, password, phone, address)
        self.__shop_name = shop_name
        self.__type = "retail"

class Manufactory(User):
    def __init__(self, id, name, email, password, phone, address, company_name):
        super().__init__(id, name, email, password, phone, address)
        self.__company_name = company_name
        self.__type = "manufactory"

class Product:
    def __init__(self, name, price, purity, quantity, manufactory):
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__purity = purity
        self.__manufactory = manufactory
    
    def store(self):
        collection = db.get_collection("product")
        new_product = {
            "name": self.__name,
            "price": self.__price,
            "purity": self.__purity,
            "quantity": self.__quantity,
            "manufactory": self.__manufactory
        }
        collection.insert_one(new_product)
        return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)

class System:
    def __init__(self):
        self.__users = []

    class Signin(APIView):
        def post(self, request):
            email = request.data.get('email')
            password = request.data.get('password')
            auth = Auth()
            user = auth.signin(email, password)
            return user

    class Signup(APIView):
        def post(self, request):
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')
            phone = request.data.get('phone')
            address = request.data.get('address')
            id = request.data.get('id')
            auth = Auth()
            payload = User(id, name, email, password, phone, address)
            user = auth.signup(payload)
            return user
    
    class Logout(APIView):
        def post(self, request):
            response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            return response

    class ShowProduct(APIView):
        def get(self, request):
            collection = db.get_collection("product")
            products = collection.find({})
            response = []
            for product in products:
                product["_id"] = str(product["_id"])
                response.append(product)
            return Response(response, status=status.HTTP_200_OK)

    class CreateProduct(APIView):
        def post(self, request):
            token = request.COOKIES.get('jwt')
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                if user and user['type'] == 'manufactory':
                    name = request.data.get('name')
                    price = request.data.get('price')
                    purity = request.data.get('purity')
                    quantity = request.data.get('quantity')
                    product = Product(name, price, purity, quantity, user)
                    user_inventory = []
                    user_inventory.append({
                    "name": name,
                    "price": price,
                    "purity": purity,
                    "quantity": quantity,
                    "manufactory": user
                    })
                    db.get_collection("user").update_one({"email": email}, {"$set": {"Inventory": user_inventory}})
                    return product.store()
                return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    class RegisterRetail(APIView):
        def post(self, request):
            token = request.COOKIES.get('jwt')
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                if user and user['type'] == 'retail':
                    return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
                name = payload['name']
                email = payload['email']
                password = payload['password']
                phone = payload['phone']
                address = payload['address']
                shop_name = request.data.get('shop_name')
                auth = Auth()
                payload = Retail(name, email, password, phone, address, shop_name)
                collection = db.get_collection("user")
                collection.update_one({"email": email}, {"$set": {"type": "retail"}})
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    class RegisterManufactory(APIView):
        def post(self, request):
            token = request.COOKIES.get('jwt')
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                if user and user['type'] == 'manufactory':
                    return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
                name = user['name']
                email = user['email']
                password = user['password']
                phone = user['phone']
                address = user['address']
                company_name = request.data.get('company_name')
                auth = Auth()
                collection = db.get_collection("user")
                collection.update_one({"email": email}, {"$set": {"type": "manufactory"}})
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    class Purchase_retails(APIView):
        def post(self, request):
            token = request.COOKIES.get('jwt')
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                if user and user['type'] == 'retail':
                    product_id = request.data.get('product_id')
                    quantity = request.data.get('quantity')
                    collection = db.get_collection("product")
                    product = collection.find_one({"_id": ObjectId(product_id)})
                    if product and product['quantity'] >= quantity:
                        collection.update_one({"_id": ObjectId(product_id)}, {"$inc": {"quantity": -quantity}})
                        user_inventory = user['Inventory']
                        user_inventory.append({"product_id": product_id, "quantity": quantity})
                        user_transaction = user['Transaction']
                        product_name = product['name']
                        product_price = product['price']
                        product_purity = product['purity']
                        product_manufactory = product['manufactory']
                        user_transaction.append({
                            "type": "purchase",
                            "product_name": product_name,
                            "product_price": product_price,
                            "product_purity": product_purity,
                            "product_manufactory": product_manufactory,
                            "quantity": quantity,
                            "retail": user
                        })
                        db.get_collection("user").update_one({"email": email}, {"$set": {"Inventory": user_inventory, "Transaction": user_transaction}})
                        db.get_collection("selling_product").insert_one({"product": product, "quantity": quantity, "retail": user})
                        return Response({"message": "Purchase successful"}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            
    class Purchase_customer(APIView):
        def post(self, request):
            token = request.COOKIES.get('jwt')
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                if user and user['type'] == 'user':
                    product_id = request.data.get('product_id')
                    quantity = request.data.get('quantity')
                    collection = db.get_collection("product_sell")
                    product = collection.find_one({"_id": ObjectId(product_id)})
                    if product and product['quantity'] >= quantity:
                        collection.update_one({"_id": ObjectId(product_id)}, {"$inc": {"quantity": -quantity}})
                        user_inventory = user['Inventory']
                        user_inventory.append({"product_id": product_id, "quantity": quantity})
                        user_transaction = user['Transaction']
                        product_name = product['name']
                        product_price = product['price']
                        product_purity = product['purity']
                        product_manufactory = product['manufactory']
                        product__retail = product['retail']
                        user_transaction.append({
                            "type": "purchase",
                            "product_name": product_name,
                            "product_price": product_price,
                            "product_purity": product_purity,
                            "product_manufactory": product_manufactory,
                            "quantity": quantity,
                            "retail": product__retail
                        })
                        db.get_collection("user").update_one({"email": email}, {"$set": {"Inventory": user_inventory, "Transaction": user_transaction}})
                        db.get_collection("selling_product").insert_one({"product": product, "quantity": quantity, "retail": user})
                        return Response({"message": "Purchase successful"}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            
    class Sell(APIView):
        def post(self, request):
            token = request.COOKIES.get('jwt')
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                if user and user['type'] == 'retail':
                    product_id = request.data.get('product_id')
                    price = request.data.get('price')
                    quantity = request.data.get('quantity')

                    inventory = user.get('Inventory', [])
                    product_in_inventory = None

                    for item in inventory:
                        if item['product_id'] == product_id:
                            product_in_inventory = item
                            break
                    if product_in_inventory == None:
                        return Response({"error": "Product not found in inventory"}, status=status.HTTP_404_NOT_FOUND)
                    if product_in_inventory['quantity'] < quantity:
                        return Response({"error": "Not enough quantity in inventory"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    collection_sell = db.get_collection("product_sell")

                    
                    new_sale_product = {
                        "name": product_in_inventory['name'],
                        "price": price,
                        "purity": product_in_inventory['purity'],
                        "quantity": quantity,
                        "manufactory": product_in_inventory['manufactory'],
                        "retail": user
                    }
                    
                    collection_sell.insert_one(new_sale_product)
                    return Response({"message": "Sell successful"}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)