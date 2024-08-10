from flask import Blueprint

logout_bp=Blueprint('logout',__name__,url_prefix='/logout')

@logout_bp.route('/')
def root_logout():
    return 'logout Page'