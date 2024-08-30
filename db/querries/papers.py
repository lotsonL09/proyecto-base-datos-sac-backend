from fastapi import HTTPException,status
from sqlalchemy import Select,func,insert,select,update,delete

from db.schemas_tables.schemas_tables import papers_table,miembros_table,paper_autor_table
from db.schemas_tables.schemas_tables import miembros_table

from extra.helper_functions import get_id_query,execute_get,execute_insert,execute_update,execute_delete

from entities.paper import Paper,Paper_update
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


def get_insert_query_title(title:str,year:int,link:str):
    insert_query=insert(papers_table).values(
        título=title,
        año=year,
        link=link
    )
    return insert_query

def get_insert_query_member(member:Member):
    insert_querry=insert(miembros_table).values(
        nombre=member.first_name,
        apellido=member.last_name,
        idCargo=4 #TODO: DEFINIR LUEGO SI MEJORAMOS ESTA PARTE
    )
    return insert_querry

def get_insert_query_paper_member(id_paper:int,id_member:int):
    insert_query=insert(paper_autor_table).values(
        paper_idP=id_paper,
        idMiembro=id_member
    )
    return insert_query

def insert_paper(title:str,link:str,year:int):
    query=get_insert_query_title(title=title,link=link,year=year)
    id=execute_insert(query=query)
    return id

def insert_member(member:Member):
    query=get_insert_query_member(member=member)
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

    id_member=execute_get(query=query)
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



def update_title(id_paper:int,title:str):
    update_query=(update(papers_table)
                .where(papers_table.c.idPaper == id_paper)
                .values(título = title))
    
    execute_update(query=update_query)

def update_link(id_paper:int,link:str):
    update_query=(update(papers_table)
                .where(papers_table.c.idPaper == id_paper)
                .values(link = link))
    
    execute_update(query=update_query)

def update_year(id_paper:int,year:int):
    update_query=(update(papers_table)
                .where(papers_table.c.idPaper == id_paper)
                .values(año = year))
    
    execute_update(query=update_query)

def add_member(id_paper:int,member:Member):

    id_member=get_id_member(member=member)

    query_insert_paper_member=get_insert_query_paper_member(id_paper=id_paper,id_member=id_member)
    _=execute_insert(query=query_insert_paper_member)

def delete_member(id_paper:int,id_member:int):
    delete_query=(delete(paper_autor_table).where(
        paper_autor_table.c.paper_idP == id_paper,
        paper_autor_table.c.idMiembro == id_member
    ))
    execute_delete(query=delete_query)

def update_register_paper(paper:Paper_update):

    if paper.title is not None:
        update_title(id_paper=paper.id,title=paper.title)
    if len(paper.members_added) != 0:
        for member in paper.members_added:
            add_member(id_paper=paper.id,member=member)
    if len(paper.members_deleted) != 0:
        for member in paper.members_deleted:
            delete_member(id_paper=paper.id,id_member=member.id)
    if paper.link is not None:
        update_link(id_paper=paper.id,link=paper.link)
    if paper.year is not None:
        update_year(id_paper=paper.id,year=paper.year.year)

    return 'Paper actualizado'



def delete_id_paper_member(id_paper:int):

    delete_query=(delete(paper_autor_table).where(
        paper_autor_table.c.paper_idP == id_paper,
    ))
    execute_delete(query=delete_query)

def delete_paper(id_paper):
    
    delete_query=(delete(papers_table).where(
        papers_table.c.idPaper == id_paper,
    ))
    execute_delete(query=delete_query)


def delete_register_paper(id_paper:int):

    #delete id_paper - id_members
    delete_id_paper_member(id_paper=id_paper)

    delete_paper(id_paper=id_paper)

    return 'Paper eliminado'
