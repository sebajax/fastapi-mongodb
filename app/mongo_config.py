"""
mongodb connection
"""

import motor
from motor.motor_asyncio import AsyncIOMotorClient


class Mongodb:
    """
    class to handle mongodb connection
    """

    def __init__(self, mongodb_url: str, database: str) -> None:
        client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
        self._db: AsyncIOMotorClient = client[database]

    def session_schema(self, schema: str):
        """
        return a session schema to be used by a repository layer
        :param schema: the schema to be used
        :type: str
        :return: the schema to be used
        :rtype: AsyncIOMotorClient
        """
        return self._db[schema]
