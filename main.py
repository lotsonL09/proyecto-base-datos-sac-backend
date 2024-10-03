from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.login import login
from routes.home import home
from routes.delete import delete
from routes.download import download
from routes.logout import logout
from routes.update import update
from routes.create import create
from routes.users import users
from routes.email import email

app=FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login)
app.include_router(home)
app.include_router(create)
app.include_router(update)
app.include_router(delete)
app.include_router(download)
app.include_router(logout)
app.include_router(users)
app.include_router(email)


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        reload=True
    )

