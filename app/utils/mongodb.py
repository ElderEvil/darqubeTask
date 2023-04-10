# utils/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = 'darqube'

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
