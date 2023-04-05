"""
user repository all the database query strings for user table
"""

from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status

from app.schemas import ServiceException


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

    async def list_items(self):
        """
        lists all the item in the database
        :return: the list of items
        :rtype: list
        """
        items = await self.session_schema.find().to_list(100)
        print(items)
        return items

    async def get_item(self, item_id: str):
        """
        creates a new item in the database
        :param item_id: to search
        :type: str
        :return: the founded id
        :rtype: dict
        """
        item = await self.session_schema.find_one({"_id": item_id})

        if item is not None:
            return item

        raise ServiceException(detail="ITEM_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)
