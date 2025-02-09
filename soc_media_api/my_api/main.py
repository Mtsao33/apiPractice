from contextlib import asynccontextmanager
from fastapi import FastAPI

#from asgi_correlation_id import CorrelationIdMiddleware

from my_api.database import database
from my_api.routers.post import router as post_router
from my_api.routers.user import router as user_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


# models are used to validate data
app = FastAPI(lifespan=lifespan)

app.include_router(
    post_router
)  # prefix="/blah" adds "/blah" in front of endpoint - modify tests to include prefix before endpoint

app.include_router(user_router)

# demonstration purposes
"""@app.get("/")
# tells api that if it gets a request at endpoint "/" it should run function root and send the value returned by root to the client
async def root():
    return {"message": "Hello, world!"}
    """


# for all workplace settings, type ctrl + shift + p and type your command into the search bar that pops up (ex: workplace settings, ruff restart server, etc)
