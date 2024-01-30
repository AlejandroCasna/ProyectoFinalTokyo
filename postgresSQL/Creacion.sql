
-- Tabla Equipo
CREATE TABLE Equipo (
    Equipo VARCHAR(500) NOT NULL,
	id_equipo VARCHAR(500) PRIMARY KEY 
);

-- Tabla Estadistica
CREATE TABLE Estadistica (
    
    equipo VARCHAR(500),
    Jugados INT,
    Sets_Jugados INT,
    Total_Puntos INT,
    Break_Puntos INT,
    Puntos_Ganados INT,
    Puntos_Perdidos INT,
    Total_Saque INT,
    Puntos_Saque INT,
    Error_Saque INT,
    Puntos_por_set_Saque double precision,
    Efic_Saque double precision,
    Total_Recepcion INT,
    Error_Recepcion INT,
    Negativo_Recepcion INT,
    Positivo_Recepcion INT,
    Excelente_Recepcion double precision,
    Efic_Recepcion double precision,
    Total_Ataque INT,
    Error_Ataque INT,
    Ataque_Bloqueado INT,
    Positivo_Ataque INT,
    Excelente_Ataque double precision,
    Efic_Ataque double precision,
    Toque_Red_Bloqueo INT,
    Puntos_de_Bloqueo INT,
    Puntos_Set_Bloqueo double precision,
    id_equipo VARCHAR(20),
    temporada VARCHAR(20),
	id_estadistica bigserial PRIMARY KEY ,
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
);

-- Tabla Clasificacion
CREATE TABLE Clasificacion (
    Posicion INT,
    equipo VARCHAR(50),
    PJ INT,
    G INT,
    P INT,
    PTS INT,
    id_equipo VARCHAR(50),
    temporada VARCHAR(50),
	id_clasificacion bigserial PRIMARY KEY ,
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
);

-- Tabla Jornadas
CREATE TABLE Jornadas (
    fecha DATE,
    hora TIME,
    equipo_local VARCHAR(255),
    resultado VARCHAR(255),
    equipo_visitante VARCHAR(255),
    id_equipo_local VARCHAR(20),
    id_equipo_visitante VARCHAR(20),
	id_jornada INT,
	ID  bigserial PRIMARY KEY ,
    FOREIGN KEY (id_equipo_local) REFERENCES Equipo(id_equipo),
    FOREIGN KEY (id_equipo_visitante) REFERENCES Equipo(id_equipo));
	
	
-- Tabla Jugadores
CREATE TABLE Jugadores (
    Dorsal INT,
    Nombre VARCHAR(500),
    Posicion VARCHAR(255),
    Altura double precision,
    Ano_de_nacimiento double precision,
    Alcance_en_ataque double precision,
    Alcance_en_bloqueo double precision,
	id_jugador VARCHAR(20) PRIMARY KEY,
	temporada VARCHAR(20),
    id_equipo VARCHAR(20),
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
);

-- Tabla Opuesto
CREATE TABLE Opuesto (
    Nombre VARCHAR(500),
    Partidos_jugados INT,
    Sets_jugados INT,
    Bloqueos INT,
    Bloqueo_exitoso INT,
    Bloqueo_fallido INT,
    Total_bloqueos INT,
    Saque INT,
    Errores_Saque INT,
    Porcentaje_error INT,
    Total_saques INT,
    Ataque_exitoso INT,
    Errores_ataque INT,
    Porc_error INT,
    Total_ataques INT,
    Ataque_Ranking double precision,
    id_jugador VARCHAR(20),
    id_equipo VARCHAR(20),
    temporada VARCHAR(20),
	id_opuesto bigserial PRIMARY KEY,
    FOREIGN KEY (id_jugador) REFERENCES Jugadores(id_jugador),
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
);

-- Tabla Receptor
CREATE TABLE Receptor (
    
    Nombre VARCHAR(500),
    Partidos_jugados INT,
    Sets_jugados INT,
    Bloqueos INT,
    Bloqueo_exitoso INT,
    Bloqueo_fallido INT,
    Total_bloqueos INT,
    Saque INT,
    Errores_Saque INT,
    Porcentaje_error INT,
    Total_saques INT,
    Ataque_exitoso INT,
    Errores_ataque INT,
    Porc_error INT,
    Total_ataques INT,
    Ataque_Ranking double precision,
    id_jugador VARCHAR(20),
    id_equipo VARCHAR(20),
    temporada VARCHAR(20),
	id_receptor bigserial PRIMARY KEY,
    FOREIGN KEY (id_jugador) REFERENCES Jugadores(id_jugador),
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
);

-- Tabla Colocador
CREATE TABLE Colocador (
    
    Nombre VARCHAR(300),
    Partidos_jugados INT,
    Sets_jugados INT,
    Acciones_exitosas INT,
    Errores_colocador INT,
    _error_colocador INT, -- Asegúrate de que sea el nombre correcto, puede ser un error tipográfico
    Puntos_negativos INT,
    Puntos_positivos INT,
    Acciones_positivas INT,
    Total_acumulado INT,
    Efic_Ranking double precision,
    id_jugador VARCHAR(20),
    id_equipo VARCHAR(20),
    temporada VARCHAR(20),
	id_colocador bigserial PRIMARY KEY,
    FOREIGN KEY (id_jugador) REFERENCES Jugadores(id_jugador),
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
);

-- Tabla Central
CREATE TABLE Central (
    
    Nombre VARCHAR(255),
    Partidos_jugados INT,
    Sets_jugados INT,
    Bloqueos INT,
    Bloqueo_exitoso INT,
    Bloqueo_fallido INT,
    Total_bloqueos INT,
    Saque INT,
    Errores_Saque INT,
    Porcentaje_error INT,
    Total_saques INT,
    Ataque_exitoso INT,
    Errores_ataque INT,
    Porc_error INT,
    Total_ataques INT,
    Ataque_Ranking double precision,
    id_jugador VARCHAR(20),
    id_equipo VARCHAR(20),
    temporada VARCHAR(20),
	id_central bigserial PRIMARY KEY,
    FOREIGN KEY (id_jugador) REFERENCES Jugadores(id_jugador),
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
);

-- Tabla Libero
CREATE TABLE Libero (
    
    Nombre VARCHAR(255),
    Partidos_jugados INT,
    Sets_jugados INT,
    Recepciones INT,
    Recepciones_exitosas INT,
    Recepciones_fallidas INT,
    Recepciones_otro_jugador INT,
    Puntos_perdidos_recep INT,
    Puntos_ganados_recep INT,
    Total_puntos_recep INT,
    Recep_Ranking double precision,
    id_jugador VARCHAR(20),
    id_equipo VARCHAR(20),
    temporada VARCHAR(20),
	id_libero bigserial PRIMARY KEY ,
    FOREIGN KEY (id_jugador) REFERENCES Jugadores(id_jugador),
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo)
);


-- Creación de la tabla Temporadas
CREATE TABLE Temporadas (
    id_temporada INT PRIMARY KEY,
    temporada VARCHAR(20) UNIQUE NOT NULL
);

-- Actualización de las tablas existentes para referenciar a Temporadas
ALTER TABLE Estadistica
ADD FOREIGN KEY (temporada) REFERENCES Temporadas(temporada);

ALTER TABLE Clasificacion
ADD FOREIGN KEY (temporada) REFERENCES Temporadas(temporada);

ALTER TABLE Jugadores
ADD FOREIGN KEY (temporada) REFERENCES Temporadas(temporada);

ALTER TABLE Opuesto
ADD FOREIGN KEY (temporada) REFERENCES Temporadas(temporada);

ALTER TABLE Receptor
ADD FOREIGN KEY (temporada) REFERENCES Temporadas(temporada);

ALTER TABLE Colocador
ADD FOREIGN KEY (temporada) REFERENCES Temporadas(temporada);

ALTER TABLE Central
ADD FOREIGN KEY (temporada) REFERENCES Temporadas(temporada);

ALTER TABLE Libero
ADD FOREIGN KEY (temporada) REFERENCES Temporadas(temporada);