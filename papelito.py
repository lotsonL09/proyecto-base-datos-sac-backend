# from openpyxl import Workbook
# from openpyxl.utils import get_column_letter
# from openpyxl.styles import Alignment,Font,Border,Side


# data=[
#     {
#         "Autor": ["R. Vichnevetzky","P. Borne","A.Pupuche"],
#         "Author_extra":["A. Serrano","R. Aleman"],
#         "Estado": "Disponible",
#         "Prestado a": "NO PRESTADO",
#         "Título": "12TH World congress on scientific computation July 18-22 1988(1)",
#         "Ubicación": "Laboratorio"
#     },
#     {
#         "Autor": ["P. Borne","J. Vignes","W. Valencia"],
#         "Author_extra":["A. Serrano"],
#         "Estado": "Disponible",
#         "Prestado a": "NO PRESTADO",
#         "Título": "A hands-on guide to effective embedded design",
#         "Ubicación": "Laboratorio"
#     },
#     {
#         "Autor": ["José M. Igreja","Joao M. Lemos"],
#         "Author_extra":["W. Ipanaque","W. Ipanaque","W. Ipanaque","W. Ipanaque"],
#         "Estado": "Disponible",
#         "Prestado a": "NO PRESTADO",
#         "Título": "Adaptive Control of Solar Energy Collector Systems",
#         "Ubicación": "Oficina Ing Ipanaque"
#     },
# ]

# wb=Workbook()
# ws=wb.active

# headers=list(data[0].keys())

# ws.append(headers)

# header_font=Font(bold=1) #instancia

# aligment=Alignment(horizontal="center",vertical="center")

# thin_border=Border(
#     left=Side(style='thin'),
#     right=Side(style='thin'),
#     top=Side(style='thin'),
#     bottom=Side(style='thin')
# )

# for col_num,header in enumerate(headers,start=1):
#     ws.cell(row=1,column=col_num).font=header_font #Se implementa en los headers
#     ws.cell(row=1,column=col_num).alignment=aligment
#     ws.cell(row=1,column=col_num).border=thin_border

# row_num=2

# for entry in data:

#     #Para determinar el total de rows que se van a utilizar para esta coleccion de datos
#     n_rows=0
#     for header in headers:
#         data=entry[header]
#         if (type(data) is list) and (len(data) > n_rows):
#             n_rows=len(data)
    



# #     title=entry["Título"]
# #     authors=entry["Autor"]
# #     state=entry["Estado"]
# #     location=entry["Ubicación"]
# #     prestado_a=entry["Prestado a"]

# #     author_rows=len(authors)

# #     #Merge cells
# #     ws.merge_cells(start_row=row_num,
# #                 start_column=1,
# #                 end_row=row_num+author_rows-1,
# #                 end_column=1)
# #     ws.merge_cells(start_row=row_num,
# #                 start_column=3,
# #                 end_row=row_num+author_rows-1,
# #                 end_column=3)
# #     ws.merge_cells(start_row=row_num,
# #                 start_column=4,
# #                 end_row=row_num+author_rows-1,
# #                 end_column=4)
# #     ws.merge_cells(start_row=row_num,
# #                 start_column=5,
# #                 end_row=row_num+author_rows-1,
# #                 end_column=5)
    
# #     #Put data in the merge cells
# #     ws.cell(row=row_num,column=1).value=title
# #     ws.cell(row=row_num,column=1).alignment=aligment
# #     #ws.cell(row=row_num,column=1).border=thin_border

# #     ws.cell(row=row_num,column=3).value=state
# #     ws.cell(row=row_num,column=3).alignment=aligment
# #     #ws.cell(row=row_num,column=3).border=thin_border

# #     ws.cell(row=row_num,column=4).value=location
# #     ws.cell(row=row_num,column=4).alignment=aligment
# #     #ws.cell(row=row_num,column=4).border=thin_border

# #     ws.cell(row=row_num,column=5).value=prestado_a
# #     ws.cell(row=row_num,column=5).alignment=aligment
# #     #ws.cell(row=row_num,column=5).border=thin_border

# #     for r in range(row_num, row_num + author_rows):
# #         for c in [1, 3, 4, 5]:
# #             ws.cell(row=r, column=c).border = thin_border


# #     #Add authors to the rows
# #     for i, author in enumerate(authors):
# #         ws.cell(row=row_num+i,column=2).value=author
# #         ws.cell(row=row_num+i,column=2).alignment=aligment
# #         ws.cell(row=row_num+i,column=2).border=thin_border
# #     row_num+=author_rows

# # ws.column_dimensions[get_column_letter(1)].width=60
# # ws.column_dimensions[get_column_letter(2)].width=30
# # ws.column_dimensions[get_column_letter(3)].width=15
# # ws.column_dimensions[get_column_letter(4)].width=20
# # ws.column_dimensions[get_column_letter(5)].width=15

# # wb.save("book.xlsx")

# from sqlalchemy import delete
# from db.schemas_tables.schemas_tables import titulo_autor_table


# def get_querry_delete_title_autor(id_title:int,id_author:int):
#     return (delete(titulo_autor_table)
#     .where(titulo_autor_table.c.IdTitulo == id_title
#     ).where(titulo_autor_table.c.IdAutor == id_author))

# def get_query_delete(table:str,param:str,value):
#     return delete(table).where(
#         getattr(table.c,param) == value
#     )

# params_dict={
#     "IdTitulo":12,
#     "IdAutor":12
# }

# def get_query_delete(table:str,params:dict):
#     query=delete(table)
#     for colum_name,value in params.items():
#         query=query.where(getattr(table.c,colum_name) == value)
#     return query


#query=get_query_delete(table=titulo_autor_table,param='IdTitulo',value=1)

# print('query 1',get_querry_delete_title_autor(id_title=12,id_author=12))

# print('query 2',get_query_delete(table=titulo_autor_table,params=params_dict))

# from datetime import datetime,timezone,time,date

# time_now=datetime.now()

# print(time_now.strftime("%Y-%m-%d %H-%M-%S"))


from sqlalchemy import Select,func
from db.schemas_tables.schemas_tables import (sections_table,actions_table,
                                            records_table,usuario_table)
from extra.helper_functions import (get_data)

query_get_records=(Select(
    records_table.c.id_record,
    usuario_table.c.user_name,
    actions_table.c.message,
    sections_table.c.name,
    records_table.c.time
    )
    .join(records_table,records_table.c.id_action == actions_table.c.id_action)
    .join(usuario_table,usuario_table.c.id_usuario == records_table.c.id_user)
    .join(sections_table,sections_table.c.id_section == records_table.c.id_section))


print(get_data(query=query_get_records,section="records"))

