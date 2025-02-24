import hashlib
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from pathlib import Path
import jwt
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'nongtonklasudnaruk'
MONGO_URI = "mongodb+srv://67011392:ceiyingyai@cluster0.3tqmk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.get_database("mydb")

class System():
    def __init__(self):
        self.__users = []

    def signup(self, name, email, password, phone, address):
        url = "http://127.0.0.1:8000/api/signup/"
        payload = {
            "name": name,
            "email": email,
            "password": password,
            "phone": phone,
            "address": address
        }
        response = requests.post(url, json=payload)
        return response.json()

    def signin(self, email, password):
        url = "http://127.0.0.1:8000/api/signin/"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=payload)
        return response.json()

class Auth():
    def __init__(self, user: 'User'):
        self.__SECRET_KEY = 'nongtonklasudnaruk'

    class Signin(APIView):
        def post(self, request):
            collection = db.get_collection("user")
            email = request.data.get('email')
            password = request.data.get('password')
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = collection.find_one({"email": email, "password": password_hash})
            if user:
                token = jwt.encode({"email": email, "exp": datetime.utcnow() + timedelta(hours=24)}, SECRET_KEY, algorithm="HS256")
                response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
                response.set_cookie(key='jwt', value=token, httponly=True)
                return response
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    class Signup(APIView):
        def post(self, request):
            collection = db.get_collection("user")
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')
            phone = request.data.get('phone')
            address = request.data.get('address')
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = collection.find_one({"email": email})
            if user:
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            new_user = {
                "name": name,
                "email": email,
                "password": password_hash,
                "phone": phone,
                "address": address
            }
            collection.insert_one(new_user)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class InventoryManager:
    def __init__(self):
        self.__inventory = []

    def add_item(self, item, quantity):
        pass

class Transaction():
    def __init__(self):
        self.__balance = 0
        self.__transactions = []

    def add_transaction(self, transaction):
        pass

class User():
    def __init__(self, name, email, password, phone, address):
        self.__name = name
        self.__email = email
        self.__password = password
        self.__phone = phone
        self.__address = address
        self.__transaction = Transaction()
        self.__inventory = InventoryManager()
        self.__type = "user"

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

class retail(User):
    def __init__(self, name, email, password, phone, address, shop_name):
        super().__init__(name, email, password, phone, address)
        self.__shop_name = shop_name
        self.__type = "retail"

class Manufactory(User):
    def __init__(self, name, email, password, phone, address, company_name):
        super().__init__(name, email, password, phone, address)
        self.__company_name = company_name
        self.__type = "manufactory"

class product():
    def __init__(self, name, price, purity, quantity, manufactory):
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__purity = purity
        self.__manufactory = manufactory