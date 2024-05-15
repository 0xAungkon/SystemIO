from fastapi import FastAPI 
from .include.context import Context

app = FastAPI()
Context.app=app
# Initialize the FastAPI app instance in the Context class

@app.get("/")
async def root():
    return {"message": "Server Is Up"}

