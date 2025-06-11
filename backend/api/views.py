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
import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
MONGO_URI = os.getenv('MONGO_URI')
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
            exp_time = datetime.utcnow() + timedelta(hours=24)
            token = jwt.encode(
                {
                    "email": email, 
                    "exp": exp_time,
                    "type": user.get("type", "user"),
                    "name": user.get("name", "")
                }, 
                SECRET_KEY, 
                algorithm="HS256"
            )
            
            response = Response({
                "message": "Login successful", 
                "token": token,
                "user": {
                    "email": email,
                    "name": user.get("name", ""),
                    "type": user.get("type", "user")
                }
            }, status=status.HTTP_200_OK)
            
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
            "balance": 0,
            "Inventory": [],
            "Transaction": [],
            "type": "user"
        }
        collection.insert_one(new_user)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class User:
    def __init__(self, id, name, email, password, phone, address):
        self.__id = id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__phone = phone
        self.__address = address
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
    def __init__(self, name, price, purity, quantity, manufactory_email):
        self.__id = ObjectId()
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__purity = purity
        self.__manufactory_email = manufactory_email
    
    def store(self):
        collection = db.get_collection("product")
        new_product = {
            "_id": ObjectId(self.__id),
            "name": self.__name,
            "price": int(self.__price),
            "purity": self.__purity,
            "quantity": int(self.__quantity),
            "manufactory": self.__manufactory_email
        }
        collection.insert_one(new_product)
        return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
    
    @property
    def _id(self):
        return str(self.__id) 

def get_token(request):
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
    return token


class Deposit(APIView):
    def post(self, request):
        token = get_token(request)
        if not token:
            return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
            email = payload['email']
            user = db.get_collection("user").find_one({"email": email})
            amount = request.data.get('amount')
            user['balance'] += amount
            db.get_collection("user").update_one({"email": email}, {"$set": {"balance": user['balance']}})
            return Response({"message": "Deposit successful"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


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
                new_product = {
                    "_id": str(product['_id']),
                    "name": product['name'],
                    "price": product['price'],
                    "purity": product['purity'],
                    "quantity": product['quantity']
                }
                response.append(new_product)
            return Response(response, status=status.HTTP_200_OK)

    class CreateProduct(APIView):
        def post(self, request):
            token = get_token(request)
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
                    product.store()
                    user_inventory = user['Inventory']
                    user_inventory.append({
                    "product_id": product._id,
                    "name": name,
                    "price": price,
                    "purity": purity,
                    "quantity": quantity,
                    "manufactory": user.get('_id')
                    })
                    user_transaction = user['Transaction']
                    user_transaction.append({
                        "type": "create",
                        "product_id": product._id,
                        "name": name,
                        "price": price,
                        "purity": purity,
                        "quantity": quantity,
                        "manufactory": user.get('_id'),
                        "timestamp": datetime.now()
                    })
                    db.get_collection("user").update_one({"email": email}, {"$set": {"Transaction": user_transaction}})
                    db.get_collection("user").update_one({"email": email}, {"$set": {"Inventory": user_inventory}})
                    return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
                return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    class RegisterRetail(APIView):
        def post(self, request):
            token = get_token(request)
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                if user and user['type'] == 'retail':
                    return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
                shop_name = request.data.get('shop_name')
                collection = db.get_collection("user")
                collection.update_one({"email": email}, {"$set": {"name": shop_name}})
                collection.update_one({"email": email}, {"$set": {"type": "retail"}})
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    class RegisterManufactory(APIView):
        def post(self, request):
            token = get_token(request)
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                if user and user['type'] == 'manufactory':
                    return Response({"error": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)
                company_name = request.data.get('company_name')
                collection = db.get_collection("user")
                collection.update_one({"email": email}, {"$set": {"name": company_name}})
                collection.update_one({"email": email}, {"$set": {"type": "manufactory"}})
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    class Purchase_retails(APIView):
        def post(self, request):
            token = get_token(request)
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                
                if not (user and user['type'] == 'retail'):
                    return Response({"error": "Invalid user type"}, status=status.HTTP_401_UNAUTHORIZED)
                    
                product_id = request.data.get('product_id')
                quantity = int(request.data.get('quantity'))
                
                collection = db.get_collection("product")
                product = collection.find_one({"_id": ObjectId(product_id)})

                if not product:
                    return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
                
                if int(user['balance']) < int(product['price']):
                    return Response({"error": "Not enough balance"}, status=status.HTTP_400_BAD_REQUEST)
                    
                if int(product['quantity']) < quantity:
                    return Response({"error": "Not enough product quantity available"}, status=status.HTTP_400_BAD_REQUEST)



                manufactory = product['manufactory']
                manufactory_email = manufactory['email']
                manufactory_user = db.get_collection("user").find_one({"email": manufactory_email})
                
                if not manufactory_user:
                    return Response({"error": "Manufactory not found"}, status=status.HTTP_404_NOT_FOUND)
                
            
                collection.update_one({"_id": ObjectId(product_id)}, {"$inc": {"quantity": -quantity}})
                
                
                manufactory_inventory = manufactory_user['Inventory']
                new_manufactory_inventory = []
                manufactory_product_found = False
                
                for item in manufactory_inventory:
                    if str(item['product_id']) == str(product_id):
                        manufactory_product_found = True
                        new_quantity = int(item['quantity']) - quantity
                        if new_quantity > 0:
                            new_manufactory_inventory.append({
                                "product_id": ObjectId(product_id),
                                "name": product['name'],
                                "quantity": new_quantity,
                                "price": product['price'],
                                "purity": product['purity'],
                                "manufactory_id": manufactory['_id']  
                            })
                    else:
                        new_manufactory_inventory.append(item)
                
                if not manufactory_product_found:
                    return Response({"error": "Product not found in manufactory inventory"}, status=status.HTTP_404_NOT_FOUND)
                
                
                user_inventory = user['Inventory']
                new_user_inventory = []
                user_product_found = False
                
                for item in user_inventory:
                    if str(item['product_id']) == str(product_id):
                        user_product_found = True
                        new_user_inventory.append({
                            "product_id": ObjectId(product_id),
                            "name": product['name'],
                            "quantity": item['quantity'] + quantity,
                            "still": item['quantity'] + quantity,
                            "price": product['price'],
                            "purity": product['purity'],
                            "manufactory_id": manufactory['_id']  
                        })
                
                if not user_product_found:
                    new_user_inventory.append({
                        "product_id": ObjectId(product_id),
                        "name": product['name'],
                        "quantity": quantity,
                        "still": quantity,
                        "price": product['price'],
                        "purity": product['purity'],
                        "manufactory_id": manufactory['_id']  
                    })
                
                
                manufactory_transaction = manufactory_user['Transaction']
                manufactory_transaction.append({
                    "product_id": ObjectId(product_id),
                    "type": "sell",
                    "name": product['name'],
                    "price": product['price'],
                    "purity": product['purity'],
                    "quantity": quantity,
                    "buyer_email": email,
                    "timestamp": datetime.now()
                })
                
                user_transaction = user['Transaction']
                user_transaction.append({
                    "product_id": ObjectId(product_id),
                    "type": "buy",
                    "name": product['name'],
                    "price": product['price'],
                    "purity": product['purity'],
                    "quantity": quantity,
                    "seller_email": manufactory_email,
                    "timestamp": datetime.now()
                })
                
                
                total_price = int(product['price'])
                
                
                db.get_collection("user").update_one(
                    {"email": manufactory_email}, 
                    {"$set": {
                        "balance": manufactory_user['balance'] + total_price,
                        "Inventory": new_manufactory_inventory,
                        "Transaction": manufactory_transaction
                    }}
                )
                
                db.get_collection("user").update_one(
                    {"email": email}, 
                    {"$set": {
                        "balance": user['balance'] - total_price,
                        "Inventory": new_user_inventory,
                        "Transaction": user_transaction
                    }}
                )
                
                
                if int(product['quantity']) - int(quantity) <= 0:
                    db.get_collection("product").delete_one({"_id": ObjectId(product_id)})
                    return Response({"message": "Purchase successful, and it sold out!!!"}, status=status.HTTP_200_OK)
                
                return Response({"message": "Purchase successful"}, status=status.HTTP_200_OK)
                
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                
                print(f"Error in purchase: {str(e)}")
                return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    class Purchase_customer(APIView):
        def post(self, request):
            token = get_token(request)
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                    
                product_id = request.data.get('product_id')
                quantity = int(request.data.get('quantity'))
                
                collection = db.get_collection("product_sell")
                product = collection.find_one({"_id": ObjectId(product_id)})
                
                if not product:
                    return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
                    
                if int(user['balance']) < product['price'] * quantity:
                    return Response({"error": "Not enough balance"}, status=status.HTTP_400_BAD_REQUEST)
                    
                if int(product['quantity']) < quantity:
                    return Response({"error": "Not enough product quantity available"}, status=status.HTTP_400_BAD_REQUEST)
                
                Retail = product['retail_id']
                Retail_user = db.get_collection("user").find_one({"_id": ObjectId(Retail)})
                Retail_email = Retail_user['email']
                
                if not Retail_user:
                    return Response({"error": "Retail not found"}, status=status.HTTP_404_NOT_FOUND)
                
             
                collection.update_one({"_id": ObjectId(product_id)}, {"$inc": {"quantity": -quantity}})
                
             
                Retail_inventory = Retail_user['Inventory']
                new_Retail_inventory = []
                Retail_product_found = False
                
                for item in Retail_inventory:
                    if str(item['product_id']) == str(product_id):
                        Retail_product_found = True
                        new_quantity = item['quantity'] - quantity
                        if new_quantity > 0:
                            new_Retail_inventory.append({
                                "product_id": ObjectId(product_id),
                                "name": product['name'],
                                "quantity": new_quantity,
                                "price": product['price'],
                                "purity": product['purity'],
                                "manufactory_id": product.get('manufactory_id') or product.get('manufactory', {}).get('_id')
                            })
                    else:
                        new_Retail_inventory.append(item)
                
                if not Retail_product_found:
                    return Response({"error": "Product not found in Retail inventory"}, status=status.HTTP_404_NOT_FOUND)
                
              
                user_inventory = user['Inventory']
                new_user_inventory = []
                user_product_found = False
                
                for item in user_inventory:
                    if str(item['product_id']) == str(product_id):
                        user_product_found = True
                        new_user_inventory.append({
                            "product_id": ObjectId(product_id),
                            "name": product['name'],
                            "quantity": item['quantity'] + quantity,
                            "price": product['price'],
                            "purity": product['purity'],
                            "retail_id": Retail  
                        })
                    else:
                        new_user_inventory.append(item)
                
                if not user_product_found:
                    new_user_inventory.append({
                        "product_id": ObjectId(product_id),
                        "name": product['name'],
                        "quantity": quantity,
                        "price": product['price'],
                        "purity": product['purity'],
                        "retail_id": Retail  
                    })
                
                
                Retail_transaction = Retail_user['Transaction']
                Retail_transaction.append({
                    "product_id": ObjectId(product_id),
                    "type": "sell",
                    "name": product['name'],
                    "price": product['price'],
                    "purity": product['purity'],
                    "quantity": quantity,
                    "buyer_email": email,
                    "timestamp": datetime.now()
                })
                
               
                user_transaction = user['Transaction']
                user_transaction.append({
                    "product_id": ObjectId(product_id),
                    "type": "buy",
                    "name": product['name'],
                    "price": product['price'],
                    "purity": product['purity'],
                    "quantity": quantity,
                    "seller_email": Retail_email,
                    "timestamp": datetime.now()
                })
                
            
                total_price = product['price'] * quantity
                
             
                db.get_collection("user").update_one(
                    {"email": Retail_email}, 
                    {"$set": {
                        "balance": Retail_user['balance'] + total_price,
                        "Inventory": new_Retail_inventory,
                        "Transaction": Retail_transaction
                    }}
                )
                
                
                db.get_collection("user").update_one(
                    {"email": email}, 
                    {"$set": {
                        "balance": user['balance'] - total_price,
                        "Inventory": new_user_inventory,
                        "Transaction": user_transaction
                    }}
                )
                
                
                if product['quantity'] - quantity <= 0:
                    db.get_collection("product_sell").delete_one({"_id": ObjectId(product_id)})
                    return Response({"message": "Purchase successful, and it sold out!!!"}, status=status.HTTP_200_OK)
                
                return Response({"message": "Purchase successful"}, status=status.HTTP_200_OK)
                
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print(f"Error in purchase: {str(e)}")
                return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    class Sell(APIView):
        def post(self, request):
            token = get_token(request)
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                
                if not (user and user['type'] == 'retail'):
                    return Response({"error": "Only retail users can sell products"}, status=status.HTTP_401_UNAUTHORIZED)
                
                product_id = request.data.get('product_id')
                price = float(request.data.get('price'))
                quantity = int(request.data.get('quantity'))

                inventory = user.get('Inventory', [])
                product_found = False
                product_in_inventory = None
                new_inventory = []
                
                for item in inventory:
                    if str(item['product_id']) == str(product_id):
                        product_found = True
                        product_in_inventory = item
                        
                        if item['still'] < quantity:
                            return Response({"error": "Not enough quantity in inventory"}, 
                                            status=status.HTTP_400_BAD_REQUEST)
                        
                        updated_quantity = item['quantity'] - quantity
                        if updated_quantity > 0:
                            new_inventory.append({
                                "product_id": item['product_id'],
                                "name": item['name'],
                                "quantity": item['quantity'],
                                "still": item['still'] - quantity,
                                "price": item['price'],
                                "purity": item['purity'],
                                "manufactory_id": item.get('manufactory_id') or item.get('manufactory', {}).get('_id')
                            })
                    else:
                        new_inventory.append(item)
                        
                if not product_found:
                    return Response({"error": "Product not found in inventory"}, 
                                status=status.HTTP_404_NOT_FOUND)
                
                collection_sell = db.get_collection("product_sell")
                db.get_collection("user").update_one({"email": email}, {"$set": {"Inventory": new_inventory}})
                manufactory_id = product_in_inventory.get('manufactory_id')
                if not manufactory_id and 'manufactory' in product_in_inventory:
                    if isinstance(product_in_inventory['manufactory'], dict):
                        manufactory_id = product_in_inventory['manufactory'].get('_id')
                match = False
                user_inventory = user['Inventory']
                for item in user['Inventory']:
                    if str(item['product_id']) == str(product_id):
                        user_inventory.remove(item)
                        db.get_collection("product_sell").delete_one({"_id": ObjectId(product_id)})
                        new_sale_product = {
                        "_id": ObjectId(item['product_id']),
                        "name": product_in_inventory['name'],
                        "price": price,
                        "purity": product_in_inventory['purity'],
                        "quantity": quantity + item['quantity'],
                        "manufactory_id": manufactory_id,
                        "retail_id": user['_id']}
                        user_inventory.append(new_sale_product)
                        match = True

                if not match:
                    new_sale_product = {
                        "_id": ObjectId(item['product_id']),
                        "name": product_in_inventory['name'],
                        "price": price,
                        "purity": product_in_inventory['purity'],
                        "quantity": quantity,
                        "manufactory_id": manufactory_id,
                        "retail_id": user['_id']
                    }
                    user_inventory.append(new_sale_product)
                
                result = collection_sell.insert_one(new_sale_product)
                
                db.get_collection("user").update_one(
                    {"email": email},
                    {"$set": {"Inventory": new_inventory}}
                )
                
                transaction = {
                    "product_id": result.inserted_id,
                    "type": "list_for_sale",
                    "name": product_in_inventory['name'],
                    "price": price,
                    "purity": product_in_inventory['purity'],
                    "quantity": quantity,
                    "timestamp": datetime.now()
                }
                
                db.get_collection("user").update_one(
                    {"email": email},
                    {"$push": {"Transaction": transaction}}
                )
                
                return Response({
                    "message": "Product listed for sale successfully",
                    "product_id": str(result.inserted_id)
                }, status=status.HTTP_201_CREATED)
                
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print(f"Error in sell: {str(e)}")
                return Response({"error": f"An unexpected error occurred: {str(e)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    class Show_list_manufactory(APIView):
        def get(self, request):
            collection = db.get_collection("user")
            manufactory = collection.find({"type": "manufactory"})
            response = []
            response.append(manufactory)
            return Response(response, status=status.HTTP_200_OK)

    class Show_item_sell(APIView):
        def get(self, request):
            collection = db.get_collection("product_sell")
            products = collection.find({})
            response = []
            for product in products:
                new_product = {
                    "_id": str(product['_id']),
                    "name": product['name'],
                    "price": product['price'],
                    "purity": product['purity'],
                    "quantity": product['quantity'],
                    "manufactory_id": str(product['manufactory_id']),
                    "retail_id": str(product['retail_id'])
                }
                response.append(new_product)
            return Response(response, status=status.HTTP_200_OK)

    class Show_item_inventory(APIView):
        def get(self, request):
            token = get_token(request)
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                inventory = user.get('Inventory', [])
                response = []
                for item in inventory:
                    manufactory_id = item.get('manufactory_id', {})
                    manufactory = db.get_collection("user").find_one({"_id": ObjectId(manufactory_id)})
                    manufactory_name = manufactory.get('name', "")
                    new_item = {
                        "product_id": str(item.get("product_id", "")),
                        "name": item.get("name", ""),
                        "price": item.get("price", ""),
                        "purity": item.get("purity", ""),
                        "still": item.get("still", ""),
                        "quantity": item.get("quantity", ""),
                        "manufactory_id": manufactory_name,
                        "retail_id": str(item.get("retail_id", ""))
                    }
                    response.append(new_item)
                return Response(response, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    class Show_item_transaction(APIView):
        def get(self, request):
            token = get_token(request)
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email})
                transaction = user.get('Transaction', [])
                response = []
                for item in transaction:
                    new_item = {
                        "product_id": str(item.get("product_id", "")),
                        "type": item.get("type", ""),
                        "name": item.get("name", ""),
                        "price": item.get("price", ""),
                        "purity": item.get("purity", ""),
                        "quantity": item.get("quantity", ""),
                        "timestamp": item.get("timestamp", "")
                    }
                    response.append(new_item)
                return Response(response, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            
    class show_name(APIView):
        def post(self, request):
            id = request.data.get('id')
            if not id:
                return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                collection = db.get_collection("user")
                user = collection.find_one({"_id": ObjectId(id)}, {"name": 1, "_id": 0}) 
                
                if not user:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                
                return Response(user, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    class UserProfile(APIView):
        def get(self, request):
            token = get_token(request)
            if not token:
                return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                email = payload['email']
                user = db.get_collection("user").find_one({"email": email}, {"_id": 0, "password": 0})
                if not user:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                inventory = user.get('Inventory', [])
                transaction = user.get('Transaction', [])
                inventory_json = []
                transaction_json = []

                for item in inventory:
                    inventory_json.append({
                        "product_id": str(item.get("product_id", "")),
                        "name": item.get("name", ""),
                        "price": item.get("price", ""),
                        "purity": item.get("purity", ""),
                        "quantity": item.get("quantity", ""),
                        "still": item.get("still", ""),
                        "manufactory_id": str(item.get("manufactory_id", "")),
                        "retail_id": str(item.get("retail_id", ""))
                    })
                for item in transaction:
                    transaction_json.append({
                        "product_id": str(item.get("product_id", "")),
                        "type": item.get("type", ""),
                        "name": item.get("name", ""),
                        "price": item.get("price", ""),
                        "purity": item.get("purity", ""),
                        "quantity": item.get("quantity", ""),
                        "timestamp": item.get("timestamp", "")
                    })
                user_json = {
                    "name": user.get("name", ""),
                    "email": user.get("email", ""),
                    "phone": user.get("phone", ""),
                    "address": user.get("address", ""),
                    "balance": user.get("balance", 0),
                    "type": user.get("type", "user"),
                    "Inventory": inventory_json,
                    "Transaction": transaction_json
                }
                return Response(user_json, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)