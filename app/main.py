from dotenv import load_dotenv
from litestar import Litestar
from litestar.config.cors import CORSConfig
from contextlib import asynccontextmanager
from app.db import get_db_client
from app.shared import logger, logging_config
from litestar.openapi import OpenAPIConfig
import uvicorn

from litestar import Router
from app.users.controllers import UserController


def create_router() -> Router:
    return Router(path='/v1', route_handlers=[UserController])


__all__ = ['create_app']

load_dotenv()
cors_config = CORSConfig(allow_origins=['*'])


@asynccontextmanager
async def lifespan(app: Litestar):
    client = app.state.mongodb_client = get_db_client()
    logger.info('Successfully Connected to Database')
    try:
        yield
    finally:
        client.close()


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[create_router()],
        cors_config=cors_config,
        lifespan=[lifespan],
        logging_config=logging_config,
        debug=True,
        openapi_config=OpenAPIConfig(title="MCQ4U API Documentation", version="1.0.0")
    )


app = create_app()

if __name__ == '__main__':
    # @TODO to configure port
    uvicorn.run(
        app,
    )
