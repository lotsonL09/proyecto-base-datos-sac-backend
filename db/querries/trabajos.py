from sqlalchemy import Select,desc

from db.schemas_tables.schemas_tables import trabajos_table,cursos_table

querry_get_trabajos=(Select(
    trabajos_table.c.Título,
    cursos_table.c.Curso,
    trabajos_table.c.Año,
    trabajos_table.c.Link)
    .join(cursos_table,cursos_table.c.idCurso  ==  trabajos_table.c.idCurso )
    .filter(trabajos_table.c.Link != 'NOT_FOUND')
    .order_by(trabajos_table.c.Año.asc(),cursos_table.c.Curso.desc()
    )
)

