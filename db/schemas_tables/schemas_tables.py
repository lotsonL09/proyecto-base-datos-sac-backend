from sqlalchemy import (Table,Column, Integer,
                        String,CheckConstraint,
                        Boolean,MetaData,
                        ForeignKey,UniqueConstraint,
                        DateTime)

metadata_obj=MetaData()

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

libro_table=Table(
    'libro',
    metadata_obj,
    Column('IdLibro',Integer,primary_key=True,autoincrement=True),
    Column('Titulo',String),
    Column('IdUbi',ForeignKey('ubicación.IdUbi')),
    Column('IdEstado',ForeignKey('estado.IdEstado')),
    Column('Cantidad',String),
)

libro_autor_table=Table(
    'libro_autor',
    metadata_obj,
    Column('IdLibro',ForeignKey('libro.IdLibro'),primary_key=True),
    Column('IdAutor',ForeignKey('autor.IdAutor'),primary_key=True)
)

libro_usuario_table=Table(
    'libro_usuario',
    metadata_obj,
    Column('IdLibro',ForeignKey('libro.IdLibro'),primary_key=True),
    Column('IdUsuario',ForeignKey('Usuario.id_usuario'),primary_key=True)
)

tipo_table=Table(
    'tipo',
    metadata_obj,
    Column('IdTipo',Integer,primary_key=True,autoincrement=True),
    Column('Tipo',String(100))
)

equipo_table=Table(
    'equipo',
    metadata_obj,
    Column('IdEquipo',Integer,primary_key=True,autoincrement=True),
    Column('Equipo',String(100)),
    Column('Descripcion',String(1000)),
    Column('Evidencia',String(250)),
    Column('Procedencia',String(200)),
    Column('Año_adquisicion',String(50)),
    Column('IdTipo',Integer,ForeignKey('tipo.IdTipo')),
    Column('IdUbi',Integer,ForeignKey('ubicación.IdUbi')),
    Column('IdEstado',Integer,ForeignKey('estado.IdEstado')),
)

estatus_table=Table(
    'Estatus',
    metadata_obj,
    Column('idEstatus',Integer,primary_key=True,autoincrement=True),
    Column('Estatus',String(45))
)

cursos_table=Table(
    'Cursos',
    metadata_obj,
    Column('idCurso',Integer,primary_key=True,autoincrement=True),
    Column('Curso',String(45))
)

convenios_table=Table(
    'Convenios',
    metadata_obj,
    Column('idConv',Integer,primary_key=True,autoincrement=True),
    Column('Convenio',String(45))
)

papers_table=Table(
    'Papers',
    metadata_obj,
    Column('idPaper',Integer,primary_key=True,autoincrement=True),
    Column('título',String(200)),
    Column('año',Integer,CheckConstraint('año >= 1000 AND año <= 9999')),
    Column('link',String(100))
)

cargos_table=Table(
    'cargos',
    metadata_obj,
    Column('idCargo',Integer,primary_key=True,autoincrement=True),
    Column('cargo',String(40))
)

miembros_table=Table(
    'Miembros',
    metadata_obj,
    Column('idMiembro',Integer,primary_key=True,autoincrement=True),
    Column('nombre',String(45)),
    Column('apellido',String(45)),
    Column('idCargo',Integer,ForeignKey('cargos.idCargo'))
)

trabajos_table=Table(
    'Trabajos',
    metadata_obj,
    Column('idTrab',Integer,primary_key=True,autoincrement=True),
    Column('Título',String(500)),
    Column('idCurso',Integer,ForeignKey('cursos.idCurso')),
    Column('Año',String(100)),
    Column('Link',String(250))
)

proyectos_table=Table(
    'Proyectos',
    metadata_obj,
    Column('idProyec',Integer,primary_key=True,autoincrement=True),
    Column('Proyecto',String(300)),
    Column('Estatus_idEst',Integer,ForeignKey('estatus.idEstatus')),
    Column('Director_idDir',Integer,ForeignKey('miembros.idMiembro')),
    Column('Año_in',String(50)),
    Column('Año_fin',String(50)),
)

proyec_conv_table=Table(
    'Proyec_Conv',
    metadata_obj,
    Column('Proyec_idP',Integer,ForeignKey('proyectos.idProyec'),primary_key=True),
    Column('Conv_idC',Integer,ForeignKey('convenios.idConv'),primary_key=True),
)

proyec_invest_table=Table(
    'Proyec_Invest',
    metadata_obj,
    Column('Proyec_idP',Integer,ForeignKey('proyectos.idProyec'),primary_key=True),
    Column('idMiembro',Integer,ForeignKey('miembros.idMiembro'),primary_key=True),
)

paper_autor_table=Table(
    'Paper_Autor',
    metadata_obj,
    Column('paper_idP',Integer,ForeignKey('proyectos.idProyec'),primary_key=True),
    Column('idMiembro',Integer,ForeignKey('miembros.idMiembro'),primary_key=True),
)

sections_table=Table(
    'sections',
    metadata_obj,
    Column('id_section',Integer,primary_key=True,autoincrement=True),
    Column('name',String),
    Column('table_name',String),
    UniqueConstraint('name',name='section_name')
)

actions_table=Table(
    'actions',
    metadata_obj,
    Column('id_action',Integer,primary_key=True,autoincrement=True),
    Column('action',String),
    Column('message',String),
    UniqueConstraint('action',name='unique_section')
)

roles_table=Table(
    'roles',
    metadata_obj,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('name',String(50))
)

usuario_table=Table(
    'Usuario',
    metadata_obj,
    Column('id_usuario',Integer,primary_key=True,autoincrement=True),
    Column('user_name',String(100)),
    Column('password',String(100)),
    Column('first_name',String(100)),
    Column('last_name',String(100)),
    Column('email',String(100)),
    Column('id_role',Integer,ForeignKey('roles.id')),
    Column('phone',String(20)),
    Column('refresh_token',String(250)),
    Column('disabled',Boolean),
    UniqueConstraint('user_name',name="uc_users"),
    UniqueConstraint('email',name="uc_email"),
)

records_table=Table(
    'records',
    metadata_obj,
    Column('id_record',Integer,primary_key=True,autoincrement=True),
    Column('id_user',Integer,ForeignKey('usuario.id_usuario')),
    Column('id_section',Integer,ForeignKey('sections.id_section')),
    Column('id_action',Integer,ForeignKey('actions.id_action')),
    Column('id_on_section',Integer),
    Column('time',DateTime)
)