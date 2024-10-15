from sqlalchemy import Select,func
from db.schemas_tables.schemas_tables import (sections_table,actions_table,
                                            records_table,usuario_table)
from extra.helper_functions import (get_data)

query_get_records=(Select(
    records_table.c.id_record,
    usuario_table.c.user_name,
    actions_table.c.message,
    sections_table.c.name,
    records_table.c.time,
    sections_table.c.table_name,
    records_table.c.id_on_section
    )
    .join(records_table,records_table.c.id_action == actions_table.c.id_action)
    .join(usuario_table,usuario_table.c.id_usuario == records_table.c.id_user)
    .join(sections_table,sections_table.c.id_section == records_table.c.id_section))


def get_records_user(user_name:str):
    query=query_get_records.where(usuario_table.c.user_name == user_name)
    return get_data(section='records',query=query)
