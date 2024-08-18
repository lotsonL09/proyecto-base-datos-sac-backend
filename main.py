from fastapi import FastAPI
import uvicorn
#from flask import Flask

from routes.login import login
from routes.home import home
from routes.delete import delete
from routes.download import download
from routes.logout import logout
from routes.update import update
from routes.edit import edit

#app=Flask(__name__)

app=FastAPI()

# app.register_blueprint(login_bp)
# app.register_blueprint(home_bp)
# app.register_blueprint(delete_bp)
# app.register_blueprint(download_bp)
# app.register_blueprint(logout_bp)
# app.register_blueprint(update_bp)
# app.register_blueprint(edit_bp)

app.include_router(login)
app.include_router(home)
app.include_router(delete)
app.include_router(download)
app.include_router(logout)
app.include_router(update)
app.include_router(edit)

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        reload=True
    )

