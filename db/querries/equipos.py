from sqlalchemy import Select

from db.schemas_tables.schemas_tables import equipo_table,tipo_table,ubicacion_table,estado_table,autor_table


querry_get_equipments=(Select(
        equipo_table.c.Descripción,
        tipo_table.c.Tipo,
        equipo_table.c.Procedencia,
        equipo_table.c.Año_adquisicion,
        ubicacion_table.c.ubicacion,
        estado_table.c.estado
    )
    .select_from(equipo_table)
    .join(tipo_table        ,tipo_table.c.IdTipo       ==    equipo_table.c.IdTipo)
    .join(ubicacion_table   ,ubicacion_table.c.IdUbi   ==    equipo_table.c.IdUbi)
    .join(estado_table      ,estado_table.c.IdEstado   ==    equipo_table.c.IdEstado)
    )