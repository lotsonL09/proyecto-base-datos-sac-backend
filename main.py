from flask import Flask

from routes.login import login_bp
from routes.home import home_bp
from routes.delete import delete_bp
from routes.download import download_bp
from routes.logout import logout_bp
from routes.update import update_bp
from routes.edit import edit_bp

app=Flask(__name__)

app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(download_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(update_bp)
app.register_blueprint(edit_bp)

if __name__ == "__main__":
    app.run(debug=True)

