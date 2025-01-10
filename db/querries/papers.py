from fastapi import HTTPException,status
from sqlalchemy import Select,func,insert,select,update,delete

from db.schemas_tables.schemas_tables import papers_table,miembros_table,paper_autor_table
from db.schemas_tables.schemas_tables import miembros_table,cargos_table

from extra.helper_functions import (execute_insert,execute_update,
                                    execute_delete,get_id,get_insert_query,
                                    get_update_query,get_delete_query,
                                    get_update_query,execute_update,
                                    send_activity_record,get_data)

from entities.paper import Paper,Paper_update
from entities.share.shared import Member
from entities.user import User
from db.querries.records import create_record

query_get_papers=(Select(
    papers_table.c.idPaper,
    papers_table.c.título,
    func.aggregate_strings(
        func.concat('(',miembros_table.c.idMiembro,',',miembros_table.c.nombre,',',miembros_table.c.apellido,',',cargos_table.c.idCargo,',',cargos_table.c.cargo,')')
            .op('ORDER BY')(func.concat(miembros_table.c.nombre,',',miembros_table.c.apellido)),
        ';'
    ).label('miembros'),
    papers_table.c.año,
    papers_table.c.link)
    .join(paper_autor_table  ,   paper_autor_table.c.paper_idP == papers_table.c.idPaper       )
    .join(miembros_table     ,   miembros_table.c.idMiembro    == paper_autor_table.c.idMiembro)
    .join(cargos_table       ,   miembros_table.c.idCargo      == cargos_table.c.idCargo)
    .group_by(papers_table.c.idPaper,
            papers_table.c.título,
            papers_table.c.año,
            papers_table.c.link)
    )

def get_paper(id):
    query=query_get_papers.where(papers_table.c.idPaper == id)
    json_data=get_data(section='papers',query=query)
    try:
        return Paper(**json_data[0])
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Paper not found in database')

def get_insert_query_title(title:str,year:int,link:str):
    insert_query=get_insert_query(table=papers_table,params={'título':title,
                                                            'año':year,
                                                            'link':link})
    return insert_query

def get_insert_query_member(member:Member):
    insert_query=get_insert_query(table=miembros_table,params={'nombre':member.first_name,
                                                            'apellido':member.last_name,
                                                            'idCargo':member.cargo.id})
    return insert_query

def get_insert_query_paper_member(id_paper:int,id_member:int):
    insert_query=get_insert_query(table=paper_autor_table,params={'paper_idP':id_paper,
                                                                'idMiembro':id_member})
    return insert_query

def insert_paper(title:str,link:str,year:int):
    query=get_insert_query_title(title=title,link=link,year=year)
    id=execute_insert(query=query)
    return id

def insert_member(member:Member):
    query=get_insert_query_member(member=member)
    id=execute_insert(query=query)
    return id

def insert_paper_member(id_paper:int,id_member:int):
    query=get_insert_query_paper_member(id_paper=id_paper,
                                        id_member=id_member)
    id=execute_insert(query=query)
    
    return id

def get_id_paper(title:str,link:str,year:int):
    
    id_title=get_id(table=papers_table,filters={'título':title},param='idPaper')

    if id_title is None:
        id_title=insert_paper(title=title,
                            link=link,
                            year=year)
        return id_title
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail='Este paper ya está registrado')

def get_id_member(member:Member):

    id_member=get_id(table=miembros_table,filters={'nombre':member.first_name,'apellido':member.last_name},param='idMiembro')

    if id_member is None:
        id_member=insert_member(member=member)
        return id_member
    else:
        return id_member[0]

def create_register_paper(paper:Paper,user:User):

    id_paper=get_id_paper(title=paper.title,
                        link=paper.link,
                        year=paper.year)

    paper.id=id_paper

    for member in paper.members:
        if member.id is None:
            id_member=get_id_member(member=member)
            member.id=id_member
        _=insert_paper_member(id_member=member.id,
                            id_paper=id_paper)

    create_record(id_user=user.id,username=user.user_name,section="paper",action='create',new_data=paper)
    return {
        "message":"Paper registrado"
    }

def update_title(id_paper:int,title:str):
    query=get_update_query(table=papers_table,filters={'idPaper':id_paper},params={'título':title})
    execute_update(query=query)

def update_link(id_paper:int,link:str):
    query=get_update_query(table=papers_table,filters={'idPaper':id_paper},params={'link':link})
    execute_update(query=query)

def update_year(id_paper:int,year:int):
    query=get_update_query(table=papers_table,filters={'idPaper':id_paper},params={'año':year})
    execute_update(query=query)

def add_member(id_paper:int,member:Member) -> Member:
    
    if member.id is None:
        member.id=get_id_member(member=member)

    query_insert_paper_member=get_insert_query_paper_member(id_paper=id_paper,id_member=member.id)
    _=execute_insert(query=query_insert_paper_member)
    return member

def delete_member(id_paper:int,id_member:int):
    query=get_delete_query(table=paper_autor_table,params={'paper_idP':id_paper,'idMiembro':id_member})
    execute_delete(query=query)

def update_register_paper(paper:Paper_update,user:User):

    previous_data=get_paper(id=paper.id)

    if not previous_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Paper not found in database')

    if paper.title is not None:
        update_title(id_paper=paper.id,title=paper.title)

    if len(paper.members_added) != 0:
        for member in paper.members_added:
            member=add_member(id_paper=paper.id,member=member)
            
    if len(paper.members_deleted) != 0:
        for member in paper.members_deleted:
            delete_member(id_paper=paper.id,id_member=member.id)

    if paper.link is not None:
        update_link(id_paper=paper.id,link=paper.link)
    if paper.year is not None:
        update_year(id_paper=paper.id,year=paper.year)

    create_record(id_user=user.id,username=user.user_name,section="paper",action='update',new_data=paper,previous_data=previous_data)

    return {
        "response":"Paper actualizado"
    }

def delete_id_paper_member(id_paper:int):
    query=get_delete_query(table=paper_autor_table,params={'paper_idP':id_paper})
    execute_delete(query=query)

def delete_paper(id_paper):
    query=get_delete_query(table=papers_table,params={'idPaper':id_paper})
    execute_delete(query=query)

def delete_register_paper(id_paper:int,user:User):
    previous_data=get_paper(id=id_paper)
    delete_id_paper_member(id_paper=id_paper)

    delete_paper(id_paper=id_paper)
    create_record(id_user=user.id,username=user.user_name,section="paper",action='delete',previous_data=previous_data)
    return {
        "response":'Paper eliminado'
    }
