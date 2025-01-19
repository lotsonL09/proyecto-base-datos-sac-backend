from entities.proyect import Proyect
from entities.share.shared import Person

def fix_register(register):
    return {
            'id':int(register.split(',')[0][1:]),
            'value':register.split(',')[1][:-1]
        }

def fix_register_2(register):
    return {
            'id':int(register[0][1:]),
            'value':register[1][:-1]
        }

def fix_register_3(register):
    #print(register)
    values=register.split(',')
    id=int(values[0][1:])
    first_name=values[1]
    last_name=values[2]
    id_cargo=int(values[3])
    value_cargo=values[4][:-1]
    return {
            'id':id,
            'first_name':first_name,
            'last_name':last_name,
            'cargo':{
                'id':id_cargo,
                'value':value_cargo
            }
        }


def scheme_book(params,book_row):
    from db.querries.libros import get_borrowed_to
    book_dict=dict()
    

    borrowed=0

    for key,value in zip(params,book_row):
        
        if key == 'authors' and (len(value.split(';')) == 1):
            author=value
            book_dict[key]=[]
            book_dict[key].append(fix_register(author))
        elif key=='authors' and (len(value.split(';')) > 1):
            authors=value.split(';')
            book_dict[key]=[]
            for author in authors:
                book_dict[key].append(fix_register(author))
        elif key == 'location':
            location=value.split(';')
            book_dict[key]=fix_register_2(location)
        elif key == 'status':
            status=value.split(';')
            book_dict[key]=fix_register_2(status)
        else:
            if key == 'id':
                users_borrowed=get_borrowed_to(id_libro=value)
                if type(users_borrowed) is str:
                    borrowed=0
                else:
                    borrowed=len(users_borrowed)
                book_dict['borrowed_to']=users_borrowed
            elif key == 'amount':
                book_dict['available']=value-borrowed
            book_dict[key]=value

    return book_dict


def scheme_user(user_row):
    return {
        'id':user_row[0],
        'user_name':user_row[1],
        'first_name':user_row[2],
        'last_name':user_row[3],
        'email':user_row[4],
        'role':{
            'id':user_row[5],
            'value':user_row[6]
        },
        'phone':user_row[7],
        'disabled':user_row[8]
    }

def scheme_user_db(user_row):
    return {
        'id':user_row[0],
        'user_name':user_row[1],
        'password':user_row[2],
        'first_name':user_row[3],
        'last_name':user_row[4],
        'email':user_row[5],
        'role':{
            'id':user_row[6],
            'value':user_row[7]
        },
        'phone':user_row[8],
        'refresh_token':user_row[9],
        'disabled':user_row[10]
    }

def scheme_paper(params,paper_row):
    paper_dict=dict()
    for key,value in zip(params,paper_row):
        if key == 'members' and (len(value.split(';')) == 1):
            member=value
            paper_dict[key]=[]
            paper_dict[key].append(fix_register_3(member))
        elif key=='members' and (len(value.split(';')) > 1):
            members=value.split(';')
            paper_dict[key]=[]
            for member in members:
                paper_dict[key].append(fix_register_3(member))
        else:
            paper_dict[key]=value
    return paper_dict


def scheme_project(params,project_row):
    project_dict=dict()
    for key,value in zip(params,project_row):
        if key == 'researchers' and (len(value.split(';')) == 1):
            member=value
            project_dict[key]=[]
            project_dict[key].append(fix_register_3(member))

        elif key=='researchers' and (len(value.split(';')) > 1):
            members=value.split(';')
            project_dict[key]=[]
            for member in members:
                project_dict[key].append(fix_register_3(member))

        elif key=='coordinator':
            data_coordinator=value.split(';')
            project_dict[key]={
                'id':int(data_coordinator[0]),
                'first_name':data_coordinator[1],
                'last_name':data_coordinator[2],
                'cargo':{
                    'id':int(data_coordinator[3]),
                    'value':data_coordinator[4]
                }
            }
        elif key == 'status':
            status=value.split(';')
            project_dict[key]=fix_register_2(status)
        elif key == 'period':
            period_data=value.split(';')
            year_start=period_data[0]
            year_end=period_data[1]
            project_dict[key]={
                'year_start':period_data[0],
                'year_end':period_data[1],
                }
        else:
            project_dict[key]=value
    
    return project_dict


def scheme_trabajo(trabajo_row):
    return {
        'id':trabajo_row[0],
        'title':trabajo_row[1],
        'course':{
            'id':trabajo_row[2],
            'value':trabajo_row[3]
        },
        'year':f'{trabajo_row[4]}',
        'link':trabajo_row[5],
    }

def scheme_equipment(params,equipment_row):
    equipment_dict=dict()

    for key,value in zip(params,equipment_row):

        if key == 'location':
            location=value.split(';')
            equipment_dict[key]=fix_register_2(location)
        elif key == 'status':
            status=value.split(';')
            equipment_dict[key]=fix_register_2(status)
        elif key == 'type':
            status=value.split(';')
            equipment_dict[key]=fix_register_2(status)
        else:
            equipment_dict[key]=value

    return equipment_dict

def scheme_equipment_mongo(equipment_row):
    return {
        'id':equipment_row[0],
        'equipment':equipment_row[1],
        'description':equipment_row[2],
        'evidence':equipment_row[3],
        'origin':equipment_row[4],
        'year':equipment_row[5],
        'type':equipment_row[6],
        'location':equipment_row[7],
        'status':equipment_row[8]
    }

def scheme_book_db(book_row):
    return {
        "id_book":book_row[0],
        "title":book_row[1],
        "id_location":book_row[2],
        "id_status":book_row[3],
        "amount":book_row[4]
    }

def scheme_status_db(status_row):
    return {
        "id":status_row[0],
        "value":status_row[1]
    }

def scheme_member_db(member_row):
    #return fix_register_3(register=member_row)
    print(member_row)
    id=int(member_row[0])
    first_name=member_row[1]
    last_name=member_row[2]
    id_cargo=int(member_row[3])
    value_cargo=member_row[4]
    return {
            'id':id,
            'first_name':first_name,
            'last_name':last_name,
            'cargo':{
                'id':id_cargo,
                'value':value_cargo
            }
        }
    # return {
    #     "id":member_row[0],
    #     "first_name":member_row[1],
    #     "last_name":member_row[2]
    # }

def scheme_location_db(status_row):
    return {
        "id":status_row[0],
        "value":status_row[1]
    }

def scheme_agreement_db(status_row):
    return {
        "id":status_row[0],
        "value":status_row[1]
    }

def scheme_role_db(category_row):
    return {
        "id":category_row[0],
        "value":category_row[1]
    }

def scheme_types_db(category_row):
    return {
        "id":category_row[0],
        "value":category_row[1]
    }

def scheme_course_db(course_row):
    return {
        "id":course_row[0],
        "value":course_row[1]
    }


def scheme_proyect_to_db(proyect:Proyect,id_coordinator:int):
    return {
        "name":proyect.name,
        "id_coordinator":id_coordinator,
        "id_status":proyect.status.id,
        "period":proyect.period
    }


def scheme_record(record_row):
    return {
        'id':record_row[0],
        'user_name':record_row[1],
        'message':record_row[2],
        'table':record_row[3],
        'time':record_row[4]
    }