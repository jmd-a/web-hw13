from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts
from src.routes import users
from src.cors import setup_limiter

app = FastAPI()


def setup_limiter():
    origins = [
        "http://localhost",
        "http://localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )


setup_limiter()

app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/users')


@app.get("/")
def read_root():
    return {"message": "Hello World"}
