from fastapi import FastAPI
from config import engine
import models
import router

app = FastAPI()
app.include_router(router.router, prefix="/level", tags=["level"])
models.Base.metadata.create_all(bind=engine)


@app.get("/home")
async def root():
    return {"message": "Hello world111"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
