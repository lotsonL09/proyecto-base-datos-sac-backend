#from flask import Blueprint

from fastapi import APIRouter

#update_bp=Blueprint('update',__name__,url_prefix='/update')

update=APIRouter(prefix='/update')

@update.get('/')
def root_update():
    return 'update Page'