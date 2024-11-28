# TPI Programación 2
Trabajo final integrador de la materia Programación 2 de la carrera Licenciatura en Ciencia de Datos en la Universidad Nacional de San Martin.

# Integrantes:
[Nazareno Magallanes](https://github.com/nazarenomm), [Lautaro Terreno](https://github.com/lauterre)

# GRAN DATA: API RESTful para la Gestión de un Torneo de Fútbol Fantasy

Nuestro objetivo es el desarrollo de una API-RESTful que le permita a los usuarios interactuar con un sistema de gestión de un torneo de fútbol fantasy, similar al Gran DT. Proporciona endpoints para registrar usuarios, crear su equipo y modificarlo, consultar estadísticas de jugadores y clubes, ver el fixture del torneo, y obtener la tabla de posiciones. 
Gran DATA apunta al público argentino futbolero y busca pisar fuerte en contra de la
competencia de los fútbol fantasy.

## Herramientas usadas

- Flask: framework para la API RESTful
- JWT (Json Web Token): para autenticar a los usuarios dentro de la app
- SQLAlchemy y MySQL: para la base de datos ([Diagrama Entidad-Relación](./database/DER.pdf))
- Docker: para la virtualización y facilitar el futuro deployment
- Postman: para el testing
- Swagger: documentación automática del proyecto 

## Patrones de diseño

En este proyecto, se implementaron los siguientes patrones de diseño:

* Singleton: Se utiliza para la conexión a la base de datos, asegurando que solo exista una instancia de la conexión. También se implemento en el servicio de Fecha.
* Factory: Se utiliza para la creación de modelos de la base de datos, permitiendo la creación de objetos sin especificar la clase concreta.
* Decoradores: Se implementó el decorador para los endpoints que solo los Admin tienen acceso. Tambien es implementado para la funcionalidad de Flask y la autentificación vía JWT.
* Observer: Se implementó este patrón para el sistema de notificaciones.

## Requerimientos de alto nivel

Algunos users storys que logramos cumplir con el objetivo:
- Los usuarios podrán crear una cuenta e iniciar sesión en la plataforma
- Los usuarios podrán armar un equipo de fútbol seleccionando 11 jugadores titulares y 4
suplentes.
- Los usuarios podrán realizar cambios en su equipo durante la semana.
- Los usuarios recibirán notificaciones sobre eventos importantes, como cambios en el
estado dentro de la plantilla.
- Los usuarios podrán visualizar estadísticas para ayudarlos a seleccionar jugadores.
- Los usuarios podrán hacer predicciones sobre los resultados de los partidos (prode)

## Mejoras a futuro

A futuro, nuestro proyecto tiene varios puntos de trabajo. Como primer objetivo, debemos hacer funcionales todos los requerimientos planteados al comienzo, como armar el fixture, los torneos e implementar la tabla de posiciones del equipo.

Otra implementación futura el la del patrón de diseño Factory a la hora de crear los usuarios. Actualmente el Admin es un usuario que se le hace la modificación, eso podría manejarse con una mejor práctica de desarrollo. 

Por otro lado, se debería trabajar en el deployment de la api, en AWS o algun otro servicio cloud.

Dentro de nuestras users stories, se encontraba la creación de un prode con un sistema de cuotas similar al usado en las casas de apuestas online. Nuestro objetivo a futuro, es realizar un modelo predictivo para definir dichas cuotas. Para ello, implementaríamos toda la información previa que tenemos de los clubes, su rendimiento y resultados, para poder hacer inferencia sobre el resultado del encuentro.

A nivel seguridad, nos gustaría implementar un sistema de autenticación en dos factores a la hora de loguearse, y la confirmación en el correo electrónico a la hora de registrarse.

Finalmente, un punto que nos gustaría mejorar es la interfaz del usuario. Ninguno de los integrantes del grupo tiene experiencia ni conocimiento en desarollo UX/UI, por lo que si queremos triunfar en nuestros objetivos debemos pulir esa parte del trabajo.  

