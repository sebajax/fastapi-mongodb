"""
routing api
"""

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.config import settings
from app.item_repository import ItemRepository
from app.mongo_config import Mongodb
from app.schemas import ResponseSchema, ItemSchema, ServiceException

app = FastAPI()

mongodb_url = f'mongodb://{settings.MONGO_USER}:{settings.MONGO_PASS}@{settings.MONGO_SERVER}:{settings.MONGO_PORT}'
database = settings.MONGO_DB

mongo_db = Mongodb(mongodb_url=mongodb_url, database=database)

item_repository = ItemRepository(session_schema=mongo_db.session_schema("Items"))


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def health_check() -> JSONResponse:
    """
    api health check
    :return:
    :rtype: JSONResponse
    """
    return JSONResponse(content={
        "health": f"API {settings.PROJECT_NAME} version {settings.VERSION} is healthy"
    })


@app.get("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
async def get_item(item_id: str):
    """
    finds an item in the database
    :param item_id: to search
    :type: str
    :return: the item from the database
    :rtype: ResponseSchema
    """
    try:
        item: dict = await item_repository.get_item(item_id=item_id)
        return ResponseSchema(detail="GET_ITEM_OK", data=item)
    except ServiceException as service_exception:
        raise HTTPException(
            status_code=service_exception.status_code,
            detail=service_exception.detail
        )


@app.get("/items", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
async def list_items() -> ResponseSchema:
    """
    lists all the items from the database
    :return: a list with all the items
    :rtype: ResponseSchema
    """
    items: list = await item_repository.list_items()
    return ResponseSchema(detail="LIST_ALL_THE_ITEMS", data={"items": items})


@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema)
async def insert_item(item: ItemSchema) -> ResponseSchema:
    """
    creates a new item in the database
    :param item: data to insert into the database previously validated
    :type: ItemSchema
    :return: the created item
    :rtype: ResponseSchema
    """
    item_json: str = jsonable_encoder(item)
    created_item: dict = await item_repository.insert_item(item=item_json)
    return ResponseSchema(detail="ITEM_CREATED", data=created_item)
