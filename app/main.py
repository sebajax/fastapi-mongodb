"""
routing api
"""

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.config import settings
from app.item_repository import ItemRepository
from app.mongo_config import Mongodb
from app.schemas import ResponseSchema, ItemSchema

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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/items", status_code=201, response_model=ResponseSchema)
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
