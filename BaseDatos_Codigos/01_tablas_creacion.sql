create database SAC;
use SAC;
create table autor (
	IdAutor int not null auto_increment,
    Autor varchar(200),
    primary key (IdAutor));

create table ubicación(
	IdUbi int not null,
    ubicacion varchar(45),
    primary key(IdUbi));
    
create table estado(
	IdEstado int not null,
    estado varchar(45),
    primary key(IdEstado));

create table persona(
	IdPersona int not null auto_increment,
    Nombre varchar (75),
    Apellido varchar (75),
    Primary Key (IdPErsona));
    
create table titulo(
	IdTitulo int not null auto_increment,
    titulo varchar(300),
    cantidad int,
    primary key(Idtitulo));
    
create table libro(
	IdLibro int not null auto_increment,
    IdTitulo int,
    IdUbi int,
    IdEstado int,
    IdPersona int,
    primary key (IdLibro),
    foreign key (IdTitulo) references titulo(Idtitulo),
    foreign key (idUbi) references ubicación(idUbi),
    foreign key (IdPersona) references persona(IdPersona),
	foreign key (idEstado) references estado(idEstado));
    
create table Titulo_autor(
	IdTitulo int not null,
    IdAutor int not null,
    primary key(IdTitulo, Idautor),
	foreign key (IdTitulo) references titulo(IdTitulo),
	foreign key (idAutor) references autor(idAutor));
    
create table tipo(
	IdTipo int not null auto_increment,
    Tipo varchar(100),
    primary key(IdTipo));

create table equipo(
	IdEquipo int not null auto_increment,
    Equipo varchar(100), #CAMBIAR EN EL EXCEL QUE CREA LAS QUERIES
    Descripcion varchar(1000),
    Evidencia varchar(250),
    Procedencia varchar(200),
    Año_adquisicion varchar(50),
    IdTipo int,
    IdUbi int,
    IdEstado int,
    primary key (IdEquipo),
    foreign key (IdTipo) references tipo(IdTipo),
    foreign key (idUbi) references ubicación(idUbi),
	foreign key (idEstado) references estado(idEstado));

create table Estatus(
	idEstatus Int not null,
    Estatus varchar(45),
    primary key (idEstatus));

create table Cursos(
	idCurso Int not null,
    Curso varchar(45),
    primary key (idCurso));

create table Convenios(
	idConv int not null auto_increment,
    Convenio varchar(45),
    primary key (idConv));

create table Papers(
	idPaper int not null auto_increment,
    título varchar(200),
    año year,
    link varchar(100),
    primary key (idPaper));
    
CREATE TABLE cargos(
idCargo INT,
cargo VARCHAR(40),
PRIMARY KEY(idCargo)
);
    
create table Miembros(
	idMiembro int Not Null auto_increment,
    nombre varchar(45),
	apellido varchar(45),
    idCargo int,
    primary key(idMiembro),
    foreign key(idCargo)
		references cargos(idCargo));

create table Trabajos(
	idTrab int Not Null auto_increment,
    Título varchar(500),
    idCurso int,
    Año varchar(100),
    Link VARCHAR(250),
    primary key(idTrab),
	foreign key(idCurso)
		references cursos(idCurso));

create table Proyectos(
	idProyec int Not Null auto_increment,
    Proyecto varchar(300),
    Estatus_idEst int,
    Director_idDir int,
    Año_in VARCHAR (50),
    Año_fin VARCHAR (50),
    primary key(idProyec),
    foreign key(Estatus_idEst)
		references estatus(idEstatus),
	foreign key(Director_idDir)
		references Miembros(idMiembro));

create table Proyec_Conv(
    Proyec_idP int,
    Conv_idC int,
    primary key(Proyec_idP,Conv_idC),
    foreign key(Proyec_idP)
		references proyectos(idProyec),
	foreign key(Conv_idC)
		references convenios(idConv));

create table Proyec_Invest(
    Proyec_idP int,
    idMiembro int,
    primary key(Proyec_idP,idMiembro),
    foreign key(Proyec_idP)
		references proyectos(idProyec),
	foreign key(idMiembro)
		references Miembros(idMiembro));
        
create table Paper_Autor(
    Paper_idP int,
    idMiembro int,
    primary key(Paper_idP,idMiembro),
    foreign key(Paper_idP)
		references papers(idPaper),
	foreign key(idMiembro)
		references Miembros(idMiembro));

CREATE TABLE Usuario(
	id_usuario int not null auto_increment,
    user_name VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    category VARCHAR(100),
    phone VARCHAR(20),
    refresh_token VARCHAR(250),
    disabled bool,
    PRIMARY KEY(id_usuario)
);

CREATE TABLE sections(
	id_section INT AUTO_INCREMENT,
    name VARCHAR(200) UNIQUE,
    PRIMARY KEY(id_section)
);

CREATE TABLE actions(
	id_action INT AUTO_INCREMENT,
    action VARCHAR(200) UNIQUE,
	PRIMARY KEY(id_action)
);

CREATE TABLE records(
	id_record INT AUTO_INCREMENT,
    id_user INT,
    id_section INT,
    id_action INT,
    id_on_section INT,
    time DATETIME, #'1000-01-01 00:00:00' to '9999-12-31 23:59:59'
    FOREIGN KEY(id_user) REFERENCES usuario(id_usuario),
    FOREIGN KEY(id_section) REFERENCES sections(id_section),
    FOREIGN KEY(id_action) REFERENCES actions(id_action),
    PRIMARY KEY(id_record)
);


