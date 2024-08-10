from flask import Blueprint

edit_bp=Blueprint('edit',__name__,url_prefix='/edit')

@edit_bp.route('/')
def root_edit():
    return 'edit Page'