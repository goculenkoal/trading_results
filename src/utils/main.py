from fastapi import FastAPI

from src.api.routers.trade.trade import router

app = FastAPI(
    title='Trading Results'
)


@app.get('/')
def hello():
    return "Hello world"


app.include_router(router)
