#from flask import Blueprint

from fastapi import APIRouter

#delete_bp=Blueprint('delete',__name__,url_prefix='/delete')

delete=APIRouter(prefix='/delete')

@delete.get('/')
def root_delete():
    return 'delete Page'