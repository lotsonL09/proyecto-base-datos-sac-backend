from flask import Blueprint

login_bp=Blueprint('login',__name__,url_prefix='/')

@login_bp.route('/')
def index():
    return 'login page'


@login_bp.route('/login')
def root_login():
    return 'login page'
