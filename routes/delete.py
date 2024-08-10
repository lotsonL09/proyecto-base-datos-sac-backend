from flask import Blueprint

delete_bp=Blueprint('delete',__name__,url_prefix='/delete')

@delete_bp.route('/')
def root_delete():
    return 'delete Page'