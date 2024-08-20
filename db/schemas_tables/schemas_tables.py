from sqlalchemy import Table,Column, Integer,String,CheckConstraint,Boolean
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey

metadata_obj=MetaData()

# occupation_table=Table(
#     'Occupation',
#     metadata_obj,
#     Column('id_occupation',primary_key=True,autoincrement=True),
#     Column('occupation',String(50))
# )

# users_table=Table(
#     'Users',
#     metadata_obj,
#     Column('id_user',primary_key=True,autoincrement=True),
#     Column('user_name',String(50)),
#     Column('first_name',String(50)),
#     Column('last_name',String(50)),
#     Column('id_occupation',ForeignKey('Occupation.id_occupation')),
#     Column('birth_date',DateTime),
#     Column('photo',String(50)),
#     Column('availability',Boolean,nullable=False,default=0),
# )


autor_table = Table(
    'autor',
    metadata_obj,
    Column('IdAutor',Integer,primary_key=True,autoincrement=True),
    Column('Autor',String(200))
)

ubicacion_table=Table(
    'ubicación',
    metadata_obj,
    Column('IdUbi',primary_key=True),
    Column('ubicacion',String(45))
)

estado_table=Table(
    'estado',
    metadata_obj,
    Column('IdEstado',primary_key=True),
    Column('estado',String(45))
)

persona_table=Table(
    'persona',
    metadata_obj,
    Column('IdPersona',Integer,primary_key=True,autoincrement=True),
    Column('Nombre',String(75)),
    Column('Apellido',String(75)),
)

titulo_table=Table(
    'titulo',
    metadata_obj,
    Column('IdTitulo',Integer,primary_key=True,autoincrement=True),
    Column('Titulo',String(300)),
    Column('Cantidad',Integer)
)

libro_table=Table(
    'libro',
    metadata_obj,
    Column('IdLibro',Integer,primary_key=True,autoincrement=True),
    Column('IdTitulo',ForeignKey('libro.IdTitulo')),
    Column('IdUbi',ForeignKey('ubicación.IdUbi')),
    Column('IdPersona',ForeignKey('persona.IdPersona')),
    Column('IdEstado',ForeignKey('estado.IdEstado')),
)

titulo_autor_table=Table(
    'Titulo_autor',
    metadata_obj,
    Column('IdTitulo',ForeignKey('titulo.IdTitulo'),primary_key=True),
    Column('IdAutor',ForeignKey('autor.IdAutor'),primary_key=True)
)

tipo_table=Table(
    'tipo',
    metadata_obj,
    Column('IdTipo',primary_key=True,autoincrement=True),
    Column('Tipo',String(100))
)

equipo_table=Table(
    'equipo',
    metadata_obj,
    Column('IdEquipo',primary_key=True,autoincrement=True),
    Column('Descripción',String(100)),
    Column('Procedencia',String(200)),
    Column('Año_adquisicion',String(50)),
    Column('IdTipo',Integer,ForeignKey('tipo.IdTipo')),
    Column('IdUbi',Integer,ForeignKey('ubicación.IdUbi')),
    Column('IdEstado',Integer,ForeignKey('estado.IdEstado')),
)

estatus_table=Table(
    'Estatus',
    metadata_obj,
    Column('idEstatus',primary_key=True),
    Column('Estatus',String(45))
)

cursos_table=Table(
    'Cursos',
    metadata_obj,
    Column('idCurso',primary_key=True),
    Column('Curso',String(45))
)

convenios_table=Table(
    'Convenios',
    metadata_obj,
    Column('idConv',primary_key=True),
    Column('Convenio',String(45))
)

papers_table=Table(
    'Papers',
    metadata_obj,
    Column('idPaper',primary_key=True,autoincrement=True),
    Column('título',String(200)),
    Column('año',Integer,CheckConstraint('año >= 1000 AND año <= 9999')),
    Column('link',String(100))
)

cargos_table=Table(
    'cargos',
    metadata_obj,
    Column('idCargo',primary_key=True),
    Column('cargo',String(40))
)

miembros_table=Table(
    'Miembros',
    metadata_obj,
    Column('idMiembro',primary_key=True,autoincrement=True),
    Column('nombre',String(45)),
    Column('apellido',String(45)),
    Column('idCargo',Integer,ForeignKey('cargos.idCargo'))
)

trabajos_table=Table(
    'Trabajos',
    metadata_obj,
    Column('idTrab',primary_key=True,autoincrement=True),
    Column('Título',String(500)),
    Column('idCurso',Integer,ForeignKey('cursos.idCurso')),
    Column('Año',String(100)),
    Column('Link',String(250))
)

proyectos_table=Table(
    'Proyectos',
    metadata_obj,
    Column('idProyec',primary_key=True,autoincrement=True),
    Column('Proyecto',String(300)),
    Column('Estatus_idEst',Integer,ForeignKey('estatus.idEstatus')),
    Column('Director_idDir',Integer,ForeignKey('miembros.idMiembro')),
    Column('Año_in',String(50)),
    Column('Año_fin',String(50)),
)

proyec_conv_table=Table(
    'Proyec_Conv',
    metadata_obj,
    Column('Proyec_idP',ForeignKey('proyectos.idProyec'),primary_key=True),
    Column('Conv_idC',ForeignKey('convenios.idConv'),primary_key=True),
)

proyec_invest_table=Table(
    'Proyec_Invest',
    metadata_obj,
    Column('Proyec_idP',ForeignKey('proyectos.idProyec'),primary_key=True),
    Column('idMiembro',ForeignKey('miembros.idMiembro'),primary_key=True),
)

paper_autor_table=Table(
    'Paper_Autor',
    metadata_obj,
    Column('paper_idP',ForeignKey('proyectos.idProyec'),primary_key=True),
    Column('idMiembro',ForeignKey('miembros.idMiembro'),primary_key=True),
)

usuario_table=Table(
    'Usuario_2',
    metadata_obj,
    Column('id_usuario',Integer,primary_key=True,autoincrement=True),
    Column('user_name',String(100)),
    Column('password',String(100)),
    Column('first_name',String(100)),
    Column('last_name',String(100)),
    Column('email',String(100)),
    Column('category',String(50)),
    Column('phone',String(20)),
    Column('disabled',Boolean)
)

