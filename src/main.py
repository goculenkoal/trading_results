from fastapi import FastAPI
from src.operations.router import router as router_operation

app = FastAPI(
    title='Trading Results'
)


@app.get('/')
def hello():
    return "Hello world"


app.include_router(router_operation)
