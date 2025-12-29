from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure
from datetime import datetime
from typing import List, Optional
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Product Management API")

# CORS middleware to allow Flutter app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
# Get connection string and handle password encoding
raw_mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
# Handle password encoding for special characters
if "mongodb+srv://" in raw_mongodb_url:
    try:
        # Parse: mongodb+srv://username:password@host
        # Find the scheme
        scheme_end = raw_mongodb_url.find("://")
        if scheme_end != -1:
            scheme = raw_mongodb_url[:scheme_end]  # mongodb+srv
            rest = raw_mongodb_url[scheme_end + 3:]  # username:password@host
            
            # Find the LAST @ (this separates credentials from host)
            last_at = rest.rfind("@")
            if last_at != -1:
                credentials = rest[:last_at]  # username:password
                host_part = rest[last_at + 1:]  # host
                
                # Split credentials into username and password
                if ":" in credentials:
                    username, password = credentials.split(":", 1)
                    # URL encode the password (handles @, #, %, etc.)
                    encoded_password = quote_plus(password)
                    # Reconstruct connection string
                    MONGODB_URL = f"{scheme}://{username}:{encoded_password}@{host_part}"
                else:
                    MONGODB_URL = raw_mongodb_url
            else:
                MONGODB_URL = raw_mongodb_url
        else:
            MONGODB_URL = raw_mongodb_url
    except Exception as e:
        print(f"Error parsing MongoDB URL: {e}")
        MONGODB_URL = raw_mongodb_url
else:
    MONGODB_URL = raw_mongodb_url

DATABASE_NAME = "productdb"
COLLECTION_NAME = "products"

# Initialize MongoDB connection
client = None
db = None
products_collection = None

try:
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    products_collection = db[COLLECTION_NAME]
    # Create index on name for better query performance
    products_collection.create_index("name")
    print(f"✅ Successfully connected to MongoDB database: {DATABASE_NAME}")
except Exception as e:
    print(f"⚠️ Warning: Could not connect to MongoDB: {e}")
    print(f"Connection string used: {MONGODB_URL[:50]}...")  # Show first 50 chars for debugging

# Hardcoded valid credentials
VALID_EMAIL = "user@example.com"
VALID_PASSWORD = "Password123"


# Request/Response Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float


class ProductListResponse(BaseModel):
    success: bool
    data: List[ProductResponse]


class AddProductRequest(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)


class AddProductResponse(BaseModel):
    success: bool
    message: str


# API Endpoints
@app.post("/api/login", response_model=LoginResponse, status_code=200)
async def login(credentials: LoginRequest):
    """
    Login endpoint with hardcoded credentials.
    Valid credentials: user@example.com / Password123
    """
    if credentials.email == VALID_EMAIL and credentials.password == VALID_PASSWORD:
        return LoginResponse(success=True, message="Login successful")
    else:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Invalid email or password"}
        )


@app.get("/api/products", response_model=ProductListResponse, status_code=200)
async def get_products():
    """
    Get all products from MongoDB.
    """
    if products_collection is None:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Database connection not available"}
        )
    try:
        # Fetch all products from database
        products_cursor = products_collection.find().sort("createdAt", -1)
        products = []
        
        for product in products_cursor:
            products.append(
                ProductResponse(
                    id=str(product["_id"]),
                    name=product["name"],
                    price=product["price"]
                )
            )
        
        return ProductListResponse(success=True, data=products)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Failed to fetch products: {str(e)}"}
        )


@app.post("/api/products", response_model=AddProductResponse, status_code=201)
async def add_product(product: AddProductRequest):
    """
    Add a new product to MongoDB.
    """
    if products_collection is None:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Database connection not available"}
        )
    try:
        # Validate product data
        if not product.name or not product.name.strip():
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Invalid product data"}
            )
        
        if product.price <= 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Invalid product data"}
            )
        
        # Create product document
        product_doc = {
            "name": product.name.strip(),
            "price": float(product.price),
            "createdAt": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = products_collection.insert_one(product_doc)
        
        if result.inserted_id:
            return AddProductResponse(
                success=True,
                message="Product added successfully"
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Failed to add product"}
            )
    
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Invalid product data"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Database error: {str(e)}"}
        )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Product Management API is running"}

