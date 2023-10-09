from fastapi import FastAPI
from config import engine
import model
import router

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/home")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(router.router, prefix="/level", tags=["level"])