from redis.asyncio import StrictRedis
from typing import Optional

class RedisClient:
    def __init__(self, host: str = 'redis', port: int = 6379, db: int = 0, password: Optional[str] = None):
        """
        Initialize Redis client
        
        Args:
            host: Redis server hostname
            port: Redis server port
            db: Redis database number
            password: Redis password if authentication is required
        """
        self.redis_client = StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True)
        
    
    async def set(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        """
        Set key to hold the string value with optional expiration
        
        Args:
            key: Key name
            value: String value
            expire: Expiration time in seconds
            
        Returns:
            Boolean indicating success
        """
        return await self.redis_client.set(key, value, ex=expire)
    
    async def get(self, key: str) -> Optional[str]:
        """
        Get the value of key
        
        Args:
            key: Key name
            
        Returns:
            Value of key or None if key does not exist
        """
        return await self.redis_client.get(key)
    
    async def delete(self, *keys: str) -> int:
        """
        Delete one or more keys
        
        Args:
            *keys: Key names to delete
            
        Returns:
            Number of keys deleted
        """
        return await self.redis_client.delete(*keys)
    
    async def exists(self, *keys: str) -> int:
        """
        Check if keys exist
        
        Args:
            *keys: Key names to check
            
        Returns:
            Number of keys that exist
        """
        return await self.redis_client.exists(*keys)
    
    async def expire(self, key: str, seconds: int) -> bool:
        """
        Set a key's time to live in seconds
        
        Args:
            key: Key name
            seconds: Time to live in seconds
            
        Returns:
            Boolean indicating success
        """
        return await self.redis_client.expire(key, seconds)
    
    async def close(self) -> None:
        """
        Close the connection
        """
        await self.redis_client.close()

async def main():
    redis_client = RedisClient()
    key = "recovery_code:minhkhoi"
    value = "123456"
    # redis_client.set(key, value, expire=60)
    await redis_client.set(key, value, expire=60)
    value = await redis_client.get(key)
    print(value)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())