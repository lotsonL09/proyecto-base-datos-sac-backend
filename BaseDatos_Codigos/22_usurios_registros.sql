USE sac;
SELECT * FROM usuario;

INSERT INTO usuario(usuario,contraseña,fullname,categoria) VALUES('William','pbkdf2:sha256:260000$ZGNtjAu39Jniv9rB$6c8f16823d2bea5071f00d0a7f24eff35566c12cdb17d3f9103d2b8945e8dc05','William Valencia','Administrativo');

ALTER TABLE usuario ADD email VARCHAR(100);

UPDATE usuario SET email='willimaca09ac@gmail.com' WHERE idusuario=1;

ALTER TABLE usuario DROP COLUMN usuario;

ALTER TABLE usuario ADD user_name VARCHAR(100);

UPDATE usuario SET user_name='william' WHERE idusuario=1;