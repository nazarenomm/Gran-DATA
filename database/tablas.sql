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

CREATE TABLE clubes (
    nombre VARCHAR(100) PRIMARY KEY,
    puntos INT NOT NULL,
    partidos_jugados INT NOT NULL,
    partidos_ganados INT NOT NULL,
    partidos_empatados INT NOT NULL,
    partidos_perdidos INT NOT NULL,
    goles_favor INT NOT NULL,
    goles_contra INT NOT NULL # ir agregando
);

CREATE TABLE jugadores (
    jugador_id INT AUTO_INCREMENT PRIMARY KEY,
    club VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio INT NOT NULL,
    posicion VARCHAR(100) NOT NULL,
    FOREIGN KEY (club) REFERENCES clubes(nombre)
);

create table puntajes (
	puntaje_id int auto_increment primary key,
    jugador_id int not null,
    puntaje decimal, # se redondea
    fecha int not null,
    foreign key (jugador_id) references jugadores(jugador_id)
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
    jugadores_id JSON NOT NULL,
    Foreign Key (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (formacion) REFERENCES formaciones(formacion)
);

CREATE TABLE partidos (
    partido_id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local INT NOT NULL,
    equipo_visitante INT NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    fecha INT NOT NULL,
    FOREIGN KEY (equipo_local) REFERENCES equipos(equipo_id),
    FOREIGN KEY (equipo_visitante) REFERENCES equipos(equipo_id)
);

# despues cambiar lo nombres para mayor claridad, si es que se puede
CREATE TABLE rendimientos (
    rendimiento_id INT AUTO_INCREMENT PRIMARY KEY,
    jugador_id INT NOT NULL,
    partido_id INT NOT NULL,
    Min INT,
    Gls INT,
    Ast INT,
    PK INT,
    PKatt INT,
    Sh INT,
    SoT INT,
    xG FLOAT,
    npxG FLOAT,
    SCA INT,
    GCA INT,
    team VARCHAR(50),
    team_goals INT,
    conceded_goals INT,
    win BOOLEAN,
    tie BOOLEAN,
    match_ VARCHAR(100), # tuve que cambiar el nombre
    Total_TotDist FLOAT,
    Total_PrgDist FLOAT,
    Short_Cmp INT,
    Short_Att INT,
    Medium_Cmp INT,
    Medium_Att INT,
    Long_Cmp INT,
    Long_Att INT,
    xAG FLOAT,
    xA FLOAT,
    KP INT,
    third_1_3 INT,
    PPA INT,
    CrsPA INT,
    PrgP INT,
    Att INT,
    Live INT,
    Dead INT,
    FK INT,
    TB INT,
    Sw INT,
    Crs INT,
    TI INT,
    CK INT,
    Tackles_Tkl INT,
    Tackles_TklW INT,
    Challenges_Tkl INT,
    Challenges_Att INT,
    Challenges_Lost INT,
    Blocks_Blocks INT,
    Blocks_Sh INT,
    Blocks_Pass INT,
    Int_ INT, # aca tambien
    Clr INT,
    Err INT,
    Touches_Def_Pen INT,
    Touches_Def_3rd INT,
    Touches_Mid_3rd INT,
    Touches_Att_3rd INT,
    Touches_Att_Pen INT,
    Take_Ons_Att INT,
    Take_Ons_Succ INT,
    Carries_Carries INT,
    Carries_TotDist FLOAT,
    Carries_PrgDist FLOAT,
    Carries_PrgC INT,
    Carries_1_3 INT,
    Carries_CPA INT,
    Carries_Mis INT,
    Carries_Dis INT,
    Receiving_Rec INT,
    Receiving_PrgR INT,
    CrdY INT,
    CrdR INT,
    Crd2Y INT,
    Fls INT,
    Fld INT,
    Off INT,
    PKwon INT,
    PKcon INT,
    OG INT,
    Recov INT,
    Aerial_Duels_Won INT,
    Aerial_Duels_Lost INT,
    SoTA INT,
    GA INT,
    Saves INT,
    PSxG FLOAT,
    Launched_Cmp FLOAT,
    Launched_Att FLOAT,
    Passes_Att_GK FLOAT,
    Passes_Thr FLOAT,
    Passes_AvgLen FLOAT,
    Goal_Kicks_Att FLOAT,
    Goal_Kicks_AvgLen FLOAT,
    Crosses_Opp FLOAT,
    Crosses_Stp FLOAT,
    Sweeper_OPA INT,
    Sweeper_AvgDist FLOAT,
    FOREIGN KEY (jugador_id) REFERENCES jugadores(jugador_id),
    FOREIGN KEY (partido_id) REFERENCES partidos(partido_id)
);