from sqlalchemy import Select,insert

from db.schemas_tables.schemas_tables import usuario_table

querry_get_users=(Select(
    usuario_table.c.user_name,
    usuario_table.c.first_name,
    usuario_table.c.last_name,
    usuario_table.c.email,
    usuario_table.c.category,
    usuario_table.c.phone,
    usuario_table.c.disabled
).select_from(usuario_table)
)

querry_get_users_db=(Select(
    usuario_table.c.user_name,
    usuario_table.c.password,
    usuario_table.c.first_name,
    usuario_table.c.last_name,
    usuario_table.c.email,
    usuario_table.c.category,
    usuario_table.c.phone,
    usuario_table.c.disabled
)
)
