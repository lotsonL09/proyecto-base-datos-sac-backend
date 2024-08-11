from sqlalchemy import Select,func
from db.schemas_tables.schemas_tables import titulo_table,autor_table,ubicacion_table,estado_table,persona_table,libro_table,titulo_autor_table

#COMPROBAR

querry_get_book_mysql="""
SELECT
        libro.IdLibro,
        titulo.Titulo,
        GROUP_CONCAT(autor.Autor ORDER BY autor.Autor ASC SEPARATOR '; ') AS autores,
        ubicación.ubicacion,
        estado.estado,
        CONCAT(persona.nombre, ' ', persona.apellido) AS nombre_completo
    FROM libro
    INNER JOIN titulo ON titulo.IdTitulo = libro.IdTitulo
    INNER JOIN titulo_autor ON titulo_autor.IdTitulo = titulo.IdTitulo
    INNER JOIN autor ON autor.IdAutor = titulo_autor.IdAutor
    INNER JOIN ubicación ON ubicación.IdUbi = libro.IdUbi
    INNER JOIN estado ON estado.IdEstado = libro.IdEstado
    INNER JOIN persona ON persona.IdPersona = libro.IdPersona
    GROUP BY libro.IdLibro, titulo.Titulo, ubicación.ubicacion, estado.estado, persona.nombre, persona.apellido
"""

# func.group_concat(
#             autor_table.c.Autor,
#             ';' #separator
#             ).label('autores'),

querry_get_books=(Select(
        titulo_table.c.Titulo,
        func.aggregate_strings(autor_table.c.Autor,';').label('autores'),
        ubicacion_table.c.ubicacion,
        estado_table.c.estado,
        func.concat(persona_table.c.Nombre,' ',persona_table.c.Apellido).label('nombre_completo')
    )
    .select_from(libro_table)
    .join(titulo_table        ,titulo_table.c.IdTitulo       ==    libro_table.c.IdTitulo)
    .join(titulo_autor_table  ,titulo_autor_table.c.IdTitulo ==    titulo_table.c.IdTitulo)
    .join(autor_table         ,autor_table.c.IdAutor         ==    titulo_autor_table.c.IdAutor)
    .join(ubicacion_table     ,ubicacion_table.c.IdUbi       ==    libro_table.c.IdUbi)
    .join(estado_table        ,estado_table.c.IdEstado       ==    libro_table.c.IdEstado)
    .join(persona_table       ,persona_table.c.IdPersona     ==    libro_table.c.IdPersona)
    .group_by(
        titulo_table.c.Titulo,
        ubicacion_table.c.ubicacion,
        estado_table.c.estado,
        persona_table.c.Nombre,
        persona_table.c.Apellido)
    )

