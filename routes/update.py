from flask import Blueprint

update_bp=Blueprint('update',__name__,url_prefix='/update')

@update_bp.route('/')
def root_update():
    return 'update Page'