from config.db_config import ES_URL, ES_USERNAME, ES_PASSWORD
from elasticsearch import AsyncElasticsearch

class ElasticSearchClient:
    def __init__(self, es_url: str = ES_URL, username: str = ES_USERNAME, password: str = ES_PASSWORD):
        """
        Initialize the ElasticSearchClient with connection details.

        Args:
            es_url (str): The URL of the ElasticSearch server.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self.es_url = es_url
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        """
        Connect to the ElasticSearch server.

        Returns:
            Elasticsearch: An instance of the Elasticsearch client.
        """
        
        self.client =  AsyncElasticsearch(
            [self.es_url],
            http_auth=(self.username, self.password)
        )
    
    async def fuzzy_search(self, index: str, field: str, value: str, size: int = 10):
        """
        Perform a fuzzy search on the specified index and field.

        Args:
            index (str): The name of the index.
            field (str): The field to search.
            value (str): The value to search for.
            size (int): The maximum number of results to return.

        Returns:
            dict: The search results.
        """
        query = {
            "size": size,
            "query": {
                "match": {
                    field: {
                        "query": value,
                        "fuzziness": "AUTO"
                    }
                }
            }
        }
        return await self.client.search(index=index, body=query)

    
    async def close(self):
        """
        Close the ElasticSearch connection.
        """
        if self.client:
            await self.client.close()