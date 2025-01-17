from fastapi import APIRouter,Depends,UploadFile,File,Form

from entities.book import Book_Create
from entities.equipment import Equipment_Create,Equipment_Evidence
from entities.paper import Paper
from entities.proyect import Proyect
from entities.trabajo import Trabajo
from entities.user import User

from db.querries.libros import create_register_book
from db.querries.papers import create_register_paper
from db.querries.proyectos import create_register_proyect
from db.querries.trabajos import create_register_trabajo
from db.querries.equipos import create_register_equipment

from config.auth import auth_user

from extra.helper_functions import upload_to_cloudinary

create=APIRouter(prefix='/create')

@create.post('/equipment_evidence')
async def send_evidence(evidence:UploadFile=File(...),
                        equipment_name:str=Form(...)
                        ,user=Depends(auth_user)):
    image_content = await evidence.read()
    url_image=upload_to_cloudinary(image=image_content,
                        equipment_name=equipment_name)
    return {
        "response":"Image sent",
        "url":url_image
    }

@create.get('/')
async def root():
    return 'Create page'

@create.post('/book')
async def create_book(book:Book_Create,user=Depends(auth_user)):
    result=create_register_book(book=book,user=user)
    return result

@create.post('/equipment')
async def create_equipment(equipment:Equipment_Create,user=Depends(auth_user)):
    result=create_register_equipment(equipment=equipment,user=user)
    return result

@create.post('/paper')
async def create_paper(paper:Paper,user=Depends(auth_user)):
    result=create_register_paper(paper=paper,user=user)
    return result

@create.post('/project')
async def create_proyect(proyect:Proyect,user=Depends(auth_user)):
    result=create_register_proyect(proyect=proyect,user=user)
    return result

@create.post('/trabajo')
async def create_trabajo(trabajo:Trabajo,user=Depends(auth_user)):
    result=create_register_trabajo(trabajo=trabajo,user=user)
    return result

@create.post('/user')
async def create_user(user=Depends(auth_user)):
    print(user)
    return 'Done'