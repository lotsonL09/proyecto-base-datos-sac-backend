from sqlalchemy import Select,func

from db.schemas_tables.schemas_tables import papers_table,miembros_table,paper_autor_table


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