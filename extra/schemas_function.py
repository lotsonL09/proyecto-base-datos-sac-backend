from entities.proyect import Proyect
from entities.share.shared import Person


def scheme_user(user_row):
    return {
        'id':user_row[0],
        'user_name':user_row[1],
        'first_name':user_row[2],
        'last_name':user_row[3],
        'email':user_row[4],
        'category':user_row[5],
        'phone':user_row[6],
        'disabled':user_row[7]
    }

def scheme_user_db(user_row):
    return {
        'id':user_row[0],
        'user_name':user_row[1],
        'password':user_row[2],
        'first_name':user_row[3],
        'last_name':user_row[4],
        'email':user_row[5],
        'category':user_row[6],
        'phone':user_row[7],
        'refresh_token':user_row[8],
        'disabled':user_row[9]
    }

def scheme_book_db(book_row):
    return {
        "id_book":book_row[0],
        "id_title":book_row[1],
        "id_location":book_row[2],
        "id_status":book_row[3],
        "id_persona":book_row[4]
    }

def scheme_status_db(status_row):
    return {
        "id":status_row[0],
        "value":status_row[1]
    }

def scheme_member_db(member_row):
    return {
        "id":member_row[0],
        "first_name":member_row[1],
        "last_name":member_row[2]
    }

def scheme_location_db(status_row):
    return {
        "id":status_row[0],
        "value":status_row[1]
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
        "id_status":proyect.status,
        "period":proyect.period
    }