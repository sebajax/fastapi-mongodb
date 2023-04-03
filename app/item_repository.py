"""
user repository all the database query strings for user table
"""

from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient


@dataclass
class ItemRepository:
    """
    class to represent the item repository
    """

    session_schema: AsyncIOMotorClient

    async def insert_item(self, item: str) -> dict:
        """
        creates a new item in the database
        :param item: data to insert into the database previously validated
        :type: ItemSchema
        :return: the created item
        :rtype: dict
        """

        new_item = await self.session_schema.insert_one(item)
        created_item = await self.session_schema.find_one({"_id": new_item.inserted_id})
        return created_item
