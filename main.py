
from typing import Union
from fastapi import FastAPI, status, HTTPException
from router import route
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
app.include_router(route.router)