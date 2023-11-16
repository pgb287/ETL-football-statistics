CREATE DATABASE FUTBOL_DW;
USE FUTBOL_DW;

CREATE TABLE dim_fixture(
	id_partido int primary key,
	nro_fecha int,
	fecha_partido date,
	estadio nvarchar(50)	
);

CREATE TABLE dim_liga(
	id_liga int primary key,
	nombre nvarchar(50)
);

CREATE TABLE dim_equipos(
	id_equipo int primary key,
	nombre nvarchar(50),
	ciudad nvarchar(50)
);

CREATE TABLE dim_tiempo(
	id_tiempo int primary key,
	fecha date,
	anio int,
	mes int,
	dia int
);

CREATE TABLE fact_estadisticas(
	id_partido int,	
	id_liga int,
	id_local int,
	id_visitante int,
	id_tiempo int,
	fecha_partido date,
	gol_local int,
	gol_visitante int,
	remates_arco int,
	remates_fuera int,
	remates_total int,
	remates_bloqueados int,
	fouls int,
	corners int,
	offsides int,
	posesion int,
	amarillas int,
	rojas int,
	atajadas int,
	total_pases int,
	pases_precisos int,
	porcentaje_pases int,	
	FOREIGN KEY (id_partido) REFERENCES dim_fixture(id_partido),
	FOREIGN KEY (id_liga) REFERENCES dim_liga(id_liga),
	FOREIGN KEY (id_local) REFERENCES dim_equipos(id_equipo),
	FOREIGN KEY (id_visitante) REFERENCES dim_equipos(id_equipo),
	FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
	CONSTRAINT pk_statistics PRIMARY KEY (id_partido,id_liga,id_local,id_visitante,id_tiempo)
);

INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971188,1,'2023-08-19','Estadio Alberto J Armando')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (988672,2,'2023-08-27','Estadio Eva Peron de Junin')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971212,3,'2023-09-03','Estadio Alberto J Armando')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971229,4,'2023-09-15','Estadio Norberto Tito Tomaghello')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971237,5,'2023-09-19','Estadio Madre de Ciudades')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971252,6,'2023-09-23','Estadio Alberto J Armando')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971259,7,'2023-10-01','Estadio Alberto J Armando')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971274,8,'2023-10-10','Estadio Julio C Villagra')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971287,9,'2023-10-21','Estadio Alberto J Armando')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971299,10,'2023-10-24','Estadio Presidente Juan Domingo Per�n')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971310,11,'2023-10-28','Estadio Alberto J Armando')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971324,12,'2023-11-05','Estadio Pedro Bidegain')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971333,13,'2023-11-12','Estadio Alberto J Armando')
INSERT INTO dim_fixture(id_partido,nro_fecha,fecha_partido,estadio) VALUES (971349,14,'2023-11-26','Estadio Malvinas Argentinas')

INSERT INTO dim_liga(id_liga,nombre) VALUES (1032,'Copa de la Liga Profesional')
INSERT INTO dim_liga(id_liga,nombre) VALUES (129,'Primera Nacional')
INSERT INTO dim_liga(id_liga,nombre) VALUES (134,'Torneo Federal A')

INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (1064,'Platense','Vicente L�pez, Provincia de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (452,'Tigre','San Fernando, Provincia de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (442,'Defensa y Justicia','Florencio Varela, Provincia de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (1065,'Central Cordoba de Santiago','Provincia de Santiago del Estero')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (446,'Lanus','Lan�s, Provincia de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (451,'Boca Juniors','La Boca, Provincia de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (440,'Belgrano Cordoba','Ciudad de C�rdoba, Provincia de C�rdoba')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (441,'Union Santa Fe','Ciudad de Santa Fe, Provincia de Santa Fe')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (436,'Racing Club','Avellaneda, Provincia de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (450,'Estudiantes L.P.','La Plata, Provincia de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (460,'San Lorenzo','Capital Federal, Ciudad de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (457,'Newells Old Boys','Rosario, Provincia de Santa Fe')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (439,'Godoy Cruz','Mendoza, Provincia de Mendoza')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (474,'Sarmiento Junin','Jun�n, Provincia de Buenos Aires')
INSERT INTO dim_equipos(id_equipo,nombre,ciudad) VALUES (435,'River Plate','Nu�ez, Provincia de Buenos Aires')

INSERT INTO dim_tiempo(id_tiempo,fecha,anio,mes,dia) VALUES (1,'2023-10-28',2023,10,28)
INSERT INTO dim_tiempo(id_tiempo,fecha,anio,mes,dia) VALUES (2,'2023-10-29',2023,10,29)
INSERT INTO dim_tiempo(id_tiempo,fecha,anio,mes,dia) VALUES (3,'2023-10-30',2023,10,30)
INSERT INTO dim_tiempo(id_tiempo,fecha,anio,mes,dia) VALUES (4,'2023-10-31',2023,10,31)


 



