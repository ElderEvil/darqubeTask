from motor.motor_asyncio import AsyncIOMotorClient

from app import config

settings = config.get_settings()
# MONGO_URI = 'mongodb://localhost:27017/'
MONGO_URI = 'mongodb://root_user:password123@db:27017/'

client = AsyncIOMotorClient(MONGO_URI)
db = client.users
users_collection = db.get_collection("users_collection")
