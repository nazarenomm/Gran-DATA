create database gran_data_test;

use gran_data_test;

create table usuarios (
	usuario_id int auto_increment primary key,
    nombre varchar(80) not null,
    apellido varchar(80) not null,
    mail varchar(256) not null unique,
    contraseña varchar(256) not null,
    telefono int
);
CREATE TABLE notificaciones (
    notificacion_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    mensaje VARCHAR(200) NOT NULL,
    fecha DATETIME NOT NULL,
    leida BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

CREATE TABLE clubes (
    club_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    -- creo que esto no lo usamos
    puntos INT NOT NULL,
    partidos_jugados INT NOT NULL,
    partidos_ganados INT NOT NULL,
    partidos_empatados INT NOT NULL,
    partidos_perdidos INT NOT NULL,
    goles_favor INT NOT NULL,
    goles_contra INT NOT NULL
);

CREATE TABLE estados (
    estado VARCHAR(100) PRIMARY KEY
);

CREATE TABLE jugadores (
    jugador_id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio INT NOT NULL,
    posicion VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    FOREIGN KEY (club_id) REFERENCES clubes(club_id),
    FOREIGN KEY (estado) REFERENCES estados(estado)
);

CREATE Table formaciones (
    formacion VARCHAR(100) PRIMARY KEY,
    defensores INT NOT NULL,
    mediocampistas INT NOT NULL,
    delanteros INT NOT NULL
);

CREATE TABLE equipos (
    equipo_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    valor INT NOT NULL,
    formacion VARCHAR(100) NOT NULL,
    Foreign Key (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (formacion) REFERENCES formaciones(formacion)
);

CREATE TABLE roles (
    rol_id INT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(100) NOT NULL
);

CREATE TABLE equipo_jugador (
    equipo_jugador_id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_id INT NOT NULL,
    jugador_id INT NOT NULL,
    rol_id INT NOT NULL,
    FOREIGN KEY (equipo_id) REFERENCES equipos(equipo_id),
    FOREIGN KEY (jugador_id) REFERENCES jugadores(jugador_id),
    FOREIGN KEY (rol_id) REFERENCES roles(rol_id)
);

CREATE TABLE puntajes (
	puntaje_id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_id INT NOT NULL,
    fecha INT NOT NULL,
    puntaje INT,
    FOREIGN KEY (equipo_id) REFERENCES equipos(equipo_id)
);

CREATE TABLE partidos (
    partido_id INT AUTO_INCREMENT PRIMARY KEY,
    local_id INT NOT NULL,
    visitante_id INT NOT NULL,
    goles_local INT,
    goles_visitante INT,
    fecha INT NOT NULL,
    FOREIGN KEY (local_id) REFERENCES clubes(club_id),
    FOREIGN KEY (visitante_id) REFERENCES clubes(club_id)
);

CREATE TABLE prodes (
    prode_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    partido_id INT NOT NULL,
    goles_local INT,
    goles_visitante INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (partido_id) REFERENCES partidos(partido_id)
)

CREATE TABLE puntajes_prode (
    puntaje_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha INT NOT NULL,
    puntaje INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

CREATE TABLE torneos (
    torneo_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    fecha_creacion DATE NOT NULL
);

CREATE TABLE torneo_usuario (
    torneo_usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    torneo_id INT NOT NULL,
    usuario_id INT NOT NULL,
    es_admin BOOLEAN NOT NULL,
    victorias INT,
    empates INT,
    derrotas INT,
    FOREIGN KEY (torneo_id) REFERENCES torneos(torneo_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

CREATE TABLE rendimientos (
    rendimiento_id INT AUTO_INCREMENT PRIMARY KEY,
    jugador_id INT NOT NULL,
    partido_id INT NOT NULL,
    minutos_jugados INT,
    goles INT,
    asistencias INT,
    goles_penal INT,
    penales_ejecutados INT,
    remates INT,
    remates_arco INT,
    xG FLOAT,
    npxG FLOAT,
    ocaciones_creadas INT,
    goles_creados INT,
    -- distancia_pases FLOAT,
    -- distancia_pases_progresivos FLOAT,
    pases_cortos_completados INT,
    pases_cortos_intentados INT,
    pases_medios_completados INT,
    pases_medios_intentados INT,
    pases_largos_completados INT,
    pases_largos_intentados INT,
    xAG FLOAT,
    xA FLOAT,
    pases_clave INT,
    -- pases_ultimo_tercio INT,
    -- pases_al_area INT,
    -- centros_al_area INT,
    pases_progresivos INT,
    pases_intentados INT,
    -- pases_pelota_en_movimiento INT,
    -- pases_pelota_parada INT,
    -- pases_tiro_libre INT,
    pases_filtrados INT,
    -- cambios_frente INT,
    centros INT,
    -- laterales_ejecutados INT,
    corners_ejecutados INT,
    entradas INT,
    entradas_ganadas INT,
    -- duelos_defensivos_ganados INT,
    -- duelos_defensivos INT,
    -- duelos_defensivos_perdidos INT,
    bloqueos INT,
    remates_bloqueados INT,
    pases_bloqueados INT,
    intercepciones INT,
    despejes INT,
    errores_graves INT,
    -- toques_area_propia INT,
    -- toques_tercio_def INT,
    -- toques_tercio_med INT,
    -- toques_tercio_ata INT,
    -- toques_area_rival INT,
    gambetas_intentadas INT,
    gambetas_completadas INT,
    traslados INT,
    -- traslados_distancia FLOAT,
    -- traslados_progresivos_distancia FLOAT,
    traslados_progresivos INT,
    -- traslados_ultimo_tercio INT,
    -- traslados_al_area INT,
    -- malos_controles INT,
    -- traslados_perdidas INT,
    -- pases_recibidos INT,
    -- pases_progresivos_recibidos INT,
    tarjetas_amarillas INT,
    tarjetas_rojas INT,
    doble_amarilla INT,
    faltas INT,
    faltas_ganadas INT,
    -- Offsides INT,
    penales_ganados INT,
    penales_concedidos INT,
    goles_en_contra INT,
    recuperaciones INT,
    duelos_aereos_ganados INT,
    duelos_aereos_perdidos INT,
    remates_arco_recibidos INT,
    goles_recibidos INT,
    atajadas INT,
    PSxG FLOAT,
    -- saques_largos_completados FLOAT,
    -- saques_largos_intentados FLOAT,
    -- pases_intentados_arqueros FLOAT,
    -- pases_lanzados_mano FLOAT,
    -- distancia_promedio_saques FLOAT,
    -- saques_arco FLOAT,
    -- distancia_promedio_saques_arco FLOAT,
    centros_enfrentados FLOAT,
    centros_atajados FLOAT,
    -- acciones_def_fuera_area INT,
    -- acciones_def_fuera_area_dist_promedio FLOAT,
    puntaje INT,
    puntaje_total INT,
    FOREIGN KEY (jugador_id) REFERENCES jugadores(jugador_id),
    FOREIGN KEY (partido_id) REFERENCES partidos(partido_id)
);