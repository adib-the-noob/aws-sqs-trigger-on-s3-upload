from fastapi import FastAPI
from router import (
    s3_uploader
)

app = FastAPI()

@app.get('/')
def root():
    return {
        "message": "Hello World"
    }
    
app.include_router(
    s3_uploader.router,
    prefix="/s3",
    tags=["s3"]
)

