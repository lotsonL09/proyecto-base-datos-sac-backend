#from flask import Blueprint

from fastapi import APIRouter

#logout_bp=Blueprint('logout',__name__,url_prefix='/logout')

logout=APIRouter(prefix='/logout')

@logout.get('/')
def root_logout():
    return 'logout Page'