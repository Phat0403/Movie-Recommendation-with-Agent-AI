from typing import Any, Dict, List, Optional, Union
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId


class MongoClient:
    """MongoDB client for FastAPI applications."""
    
    def __init__(self, connection_string: str, database_name: str):
        """
        Initialize the MongoDB client.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        
    def connect(self):
        """Connect to the MongoDB database."""
        self.client = AsyncIOMotorClient(self.connection_string)
        self.db = self.client[self.database_name]
        
    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            
    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """
        Get a collection from the database.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            AsyncIOMotorCollection: The MongoDB collection
        """
        if self.db is None:
            raise ConnectionError("Database connection not established")
        return self.db[collection_name]
    
    async def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find a single document in the collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            Optional[Dict[str, Any]]: The found document or None
        """
        collection = self.get_collection(collection_name)
        return await collection.find_one(query)
    
    async def find_many(self, collection_name: str, query: Dict[str, Any], 
                         skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Find multiple documents in the collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            
        Returns:
            List[Dict[str, Any]]: List of found documents
        """
        collection = self.get_collection(collection_name)
        cursor = collection.find(query).skip(skip).limit(limit)
        return [doc async for doc in cursor]
    
    async def insert_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        """
        Insert a document into the collection.
        
        Args:
            collection_name: Name of the collection
            document: Document to insert
            
        Returns:
            str: ID of the inserted document
        """
        collection = self.get_collection(collection_name)
        result = await collection.insert_one(document)
        return str(result.inserted_id)
    
    async def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Insert multiple documents into the collection.
        
        Args:
            collection_name: Name of the collection
            documents: Documents to insert
            
        Returns:
            List[str]: IDs of the inserted documents
        """
        collection = self.get_collection(collection_name)
        result = await collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids]
    
    async def update_one(self, collection_name: str, query: Dict[str, Any], 
                          update: Dict[str, Any]) -> int:
        """
        Update a single document in the collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            
        Returns:
            int: Number of modified documents
        """
        collection = self.get_collection(collection_name)
        result = await collection.update_one(query, {"$set": update})
        return result.modified_count
    
    async def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Delete a single document from the collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            int: Number of deleted documents
        """
        collection = self.get_collection(collection_name)
        result = await collection.delete_one(query)
        return result.deleted_count
    
    async def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Delete multiple documents from the collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            int: Number of deleted documents
        """
        collection = self.get_collection(collection_name)
        result = await collection.delete_many(query)
        return result.deleted_count
    
    async def count_documents(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Count documents in the collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            int: Number of matching documents
        """
        collection = self.get_collection(collection_name)
        return await collection.count_documents(query)
    
    @staticmethod
    def object_id_to_str(obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert ObjectId to string in a document.
        
        Args:
            obj: Document with potential ObjectId
            
        Returns:
            Dict[str, Any]: Document with string IDs
        """
        if "_id" in obj and isinstance(obj["_id"], ObjectId):
            obj["_id"] = str(obj["_id"])
        return obj
    
def create_mongo_client(connection_string: str, database_name: str) -> MongoClient:
    """
    Create and configure MongoDB client for FastAPI.
    
    Args:
        app: FastAPI application
        connection_string: MongoDB connection string
        database_name: Name of the database to use
        
    Returns:
        MongoClient: Configured MongoDB client
    """
    mongo_client = MongoClient(connection_string, database_name)
    
    return mongo_client


if __name__ == "__main__":
    import asyncio
    from config.db_config import MONGO_URI, MONGO_DB_NAME

    async def test_connection():
        MONGO_URI = "mongodb://root:example@localhost:27017/?authSource=admin"
        mongo_client = create_mongo_client(MONGO_URI, MONGO_DB_NAME)
        mongo_client.connect()
        print("Connected client:", mongo_client.client)
        print("Database name:", mongo_client.db.name)
        print("Collection names:", await mongo_client.db.list_collection_names())
        # Optionally check if connected:
        try:
            server_info = await mongo_client.client.server_info()
            print("MongoDB Server Info:", server_info)
        except Exception as e:
            print("Connection failed:", e)
        await mongo_client.close()

    asyncio.run(test_connection())