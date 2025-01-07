from sqlalchemy import select

from db.schemas_tables.schemas_tables import cursos_table

from sqlalchemy.orm import sessionmaker

from db.mysql_session.db_session import engine

from extra.schemas_function import scheme_course_db

from entities.course import Course

query_get_courses=select(cursos_table)

Session=sessionmaker(engine)

def get_courses_data(query) -> list[Course]:
    all_courses=[]
    with Session() as session:
        results=session.execute(query).fetchall()
        for course in results:
            course_db=Course(**scheme_course_db(course))
            all_courses.append(course_db)
    return all_courses
