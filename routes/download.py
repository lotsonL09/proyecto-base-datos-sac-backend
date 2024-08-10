from flask import Blueprint

download_bp=Blueprint('download',__name__,url_prefix='/download')

@download_bp.route('/')
def root_download():
    return 'download Page'