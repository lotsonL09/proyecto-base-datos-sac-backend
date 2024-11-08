USE SAC;

CREATE TABLE Usuario_2(
	id_usuario int not null auto_increment,
    user_name VARCHAR(100),
    password VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    category VARCHAR(100),
    phone VARCHAR(20),
    refresh_token VARCHAR(250),
    disabled bool,
    PRIMARY KEY(id_usuario)
);

ALTER TABLE Usuario_2
ADD CONSTRAINT uc_users UNIQUE(user_name);

ALTER TABLE Usuario_2
ADD CONSTRAINT uc_email UNIQUE(email);

#DONE

ALTER TABLE equipo
RENAME COLUMN Descripción TO Equipo;

ALTER TABLE equipo
ADD Descripcion VARCHAR(1000) AFTER Equipo;

ALTER TABLE equipo
ADD Evidencia VARCHAR(250) AFTER Descripcion;

CREATE TABLE sections(
	id_section INT AUTO_INCREMENT,
    name VARCHAR(200),
    PRIMARY KEY(id_section)
);

ALTER TABLE sections
ADD CONSTRAINT section_name UNIQUE(name);

INSERT sections(name) VALUES("books");
INSERT sections(name) VALUES("papers");
INSERT sections(name) VALUES("equipments");
INSERT sections(name) VALUES("projects");
INSERT sections(name) VALUES("trabajos");
INSERT sections(name) VALUES("users");


CREATE TABLE actions(
	id_action INT AUTO_INCREMENT,
    action VARCHAR(200),
	PRIMARY KEY(id_action)
);

ALTER TABLE actions
ADD CONSTRAINT unique_section UNIQUE(action);


INSERT actions(action) VALUES("create");
INSERT actions(action) VALUES("update");
INSERT actions(action) VALUES("delete");


CREATE TABLE records(
	id_record INT AUTO_INCREMENT,
    id_user INT,
    id_section INT,
    id_action INT,
    id_on_section INT,
    time DATETIME, #'1000-01-01 00:00:00' to '9999-12-31 23:59:59'
    FOREIGN KEY(id_user) REFERENCES usuario_2(id_usuario),
    FOREIGN KEY(id_section) REFERENCES sections(id_section),
    FOREIGN KEY(id_action) REFERENCES actions(id_action),
    PRIMARY KEY(id_record)
);


SELECT * FROM sections;

INSERT sections(name) VALUES("status_equipment");
INSERT sections(name) VALUES("status_project");
INSERT sections(name) VALUES("courses");
INSERT sections(name) VALUES("locations");



