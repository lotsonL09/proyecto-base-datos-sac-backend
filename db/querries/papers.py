from fastapi import HTTPException,status
from sqlalchemy import Select,func,insert,select,update,delete

from db.schemas_tables.schemas_tables import papers_table,miembros_table,paper_autor_table
from db.schemas_tables.schemas_tables import miembros_table

from extra.helper_functions import get_id_query,execute_get,execute_insert

from entities.paper import Paper
from entities.share.shared import Member

querry_get_papers=(Select(
    papers_table.c.idPaper,
    papers_table.c.título,
    func.aggregate_strings(
        func.concat(miembros_table.c.nombre,' ',miembros_table.c.apellido)
            .op('ORDER BY')(func.concat(miembros_table.c.nombre,' ',miembros_table.c.apellido)),
        ';'
    ).label('miembros'),
    papers_table.c.año,
    papers_table.c.link)
    .join(paper_autor_table  ,   paper_autor_table.c.paper_idP == papers_table.c.idPaper       )
    .join(miembros_table     ,   miembros_table.c.idMiembro    == paper_autor_table.c.idMiembro)
    .group_by(papers_table.c.idPaper,
            papers_table.c.título,
            papers_table.c.año,
            papers_table.c.link)
    )

query_get_id_paper=get_id_query(table=papers_table,param=papers_table.c.idPaper)

query_get_id_member=get_id_query(table=miembros_table,param=miembros_table.c.idMiembro)


def get_insert_querry_title(title:str,year:int,link:str):
    insert_query=insert(papers_table).values(
        título=title,
        año=year,
        link=link
    )
    return insert_query

def get_insert_querry_member(member:Member):
    insert_querry=insert(miembros_table).values(
        nombre=member.first_name,
        apellido=member.last_name,
        idCargo=4 #TODO: DEFINIR LUEGO SI MEJORAMOS ESTA PARTE
    )
    return insert_querry

def get_insert_query_paper_member(id_paper:int,id_member:int):
    insert_querry=insert(paper_autor_table).values(
        paper_idP=id_paper,
        idMiembro=id_member
    )
    return insert_querry

def insert_paper(title:str,link:str,year:int):
    query=get_insert_querry_title(title=title,link=link,year=year)
    id=execute_insert(query=query)
    return id

def insert_member(member:Member):
    query=get_insert_querry_member(member=member)
    print('querry utilizada',query)
    id=execute_insert(query=query)
    return id

def insert_paper_member(id_paper:int,id_member:int):
    query=get_insert_query_paper_member(id_paper=id_paper,
                                        id_member=id_member)
    id=execute_insert(query=query)
    
    return id

def get_id_paper(title:str,link:str,year:int):
    query=query_get_id_paper.where(papers_table.c.título == title)

    id_title=execute_get(querry=query)

    if id_title is None:
        id_title=insert_paper(title=title,
                            link=link,
                            year=year)
        return id_title
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail='Este paper ya está registrado')

def get_id_member(member:Member):
    query=query_get_id_member.where((miembros_table.c.nombre == member.first_name) & 
                                    (miembros_table.c.apellido == member.last_name))

    id_member=execute_get(querry=query)
    if id_member is None:
        id_member=insert_member(member=member)
        return id_member
    else:
        return id_member[0]

def create_register_paper(paper:Paper):

    id_paper=get_id_paper(title=paper.title,
                        link=paper.link,
                        year=paper.year.year)
    
    id_members=[]
    for member in paper.members:
        id_member=get_id_member(member=member)
        id_members.append(id_member)
    
    for id_member in id_members:
        _=insert_paper_member(id_member=id_member,
                            id_paper=id_paper)

    return 'Registro realizado'


def update_register_book(paper:Paper):
    print(paper.id)
    print(paper.title)
    print(paper.link)
    print(paper.members)
    
    return 'Paper actualizado'