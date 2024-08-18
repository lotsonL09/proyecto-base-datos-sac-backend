#from flask import Blueprint

from fastapi import APIRouter

#download_bp=Blueprint('download',__name__,url_prefix='/download')

download=APIRouter(prefix='/download')

@download.get('/')
def root_download():
    return 'download Page'