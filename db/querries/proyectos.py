from sqlalchemy import Select,func,distinct

from db.schemas_tables.schemas_tables import proyec_invest_table,proyectos_table,convenios_table,miembros_table,proyec_conv_table
from db.schemas_tables.schemas_tables import estatus_table

coordinador=miembros_table.alias('coordinador')
investigador=miembros_table.alias('investigador')

querry_get_proyectos=(Select(
    proyectos_table.c.idProyec,
    proyectos_table.c.Proyecto,
    func.concat(coordinador.c.nombre,' ',coordinador.c.apellido).label('Coordinador'),
    func.aggregate_strings(
        distinct(func.concat(investigador.c.nombre,' ',investigador.c.apellido))
            .op('ORDER BY')(func.concat(investigador.c.nombre,' ',investigador.c.apellido)),
        ';'
    ).label('Investigadores'),
    func.aggregate_strings(
        distinct(convenios_table.c.Convenio)
            .op('ORDER BY')(convenios_table.c.Convenio),
        ';'
    ).label('Convenios'),
    estatus_table.c.Estatus,
    proyectos_table.c.Año_in,
    proyectos_table.c.Año_fin
)
.join(proyec_invest_table   ,   proyec_invest_table.c.Proyec_idP ==   proyectos_table.c.idProyec)
.join(investigador          ,   investigador.c.idMiembro         ==   proyec_invest_table.c.idMiembro)
.join(coordinador           ,   proyectos_table.c.Director_idDir ==   coordinador.c.idMiembro)
.join(proyec_conv_table     ,   proyec_conv_table.c.Proyec_idP   ==   proyectos_table.c.idProyec)
.join(convenios_table       ,   convenios_table.c.idConv         ==   proyec_conv_table.c.Conv_idC)
.join(estatus_table         ,   estatus_table.c.idEstatus        ==   proyectos_table.c.Estatus_idEst)
.group_by(
    proyectos_table.c.idProyec,
    proyectos_table.c.Proyecto,
    estatus_table.c.Estatus,
    proyectos_table.c.Año_in,
    proyectos_table.c.Año_fin,
    coordinador.c.nombre,
    coordinador.c.apellido
)
)


