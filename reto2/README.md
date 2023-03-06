# st0263-231 Tópicos Especiales en Telemática.

## Estudiante: Simón Cárdenas Villada, scardenasv@eafit.edu.co

## Profesor: Edwin Nelson Montoya Múnera, emontoya@eafit.edu.co


# Reto 2
## 1. Breve descripción de la actividad

### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Se desarrolló una simulación de comunicación entre procesos a través de MOM y gRPC, utilizando un API Gateway que opera sobre REST para recibir las peticiones de los clientes.
Además se cuentan con archivos de configuración para los parámetros de ejecución.

## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

**Esta fue la arquitectura implementada:**

![alt text](https://github.com/[sicarvi]/[scardenasv-st0263]/blob/[master]/Pasted image 20230305201728.png?raw=true)
Se hizo uso de comunicación asincrónica para el MOM server y de comunicación sincrónica para el gRPC. Se hace una separación por capas para seccionar las responsabilidades y la arquitectura de microservicios para la implementación de los métodos ``list_files()`` y ``find_files()``.

## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Este proyecto fue desarrollado en **python** utilizando el framework de **FastAPI** para desarrollar el API Gateway REST, junto con las librerías de comunicación para RabbitMQ y gRPC.
### Configuracion RabbitMQ
Es necesario instalar rabbitmq a través de un contenedor docker:
```
docker run -d --hostname my-rabbit -p 15672:15672 -p 5672:5672 --name rabbit-server -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
```
Una vez hecho esto es necesario configurar los siguientes aspectos:
- Crear un exchange de tipo default llamado ``my_exchange``
- Crear una cola llamada ``requests``
- Hacer bind de la cola `requests` al exchange `my_exchange` con un route key `ms1`
Con esto queda configurado el servidor MOM.

Al interior del directorio de cada microservicio ``ms1`` y ``ms2`` se encuentra un archivo ``config.json`` donde se indican los puertos, direcciones IP y carpetas de archivos sobre los que trabajará cada microservicio.
Ejemplo del ``config.json`` para el ms1:
````
{

    "DIR_NAME":"example_files",

    "HOST_IP":"localhost",

    "PORT":5672

}
````
El nombre del directorio a examinar debe ser un fichero dentro de la carpeta de cada microservicio, en el ejemplo se hace referencia a una carpeta con archivos de ejemplo con ``path: ms1/example_files``.

El proyecto está configurado para funcionar a través de un entorno virtual ``pipenv``, por lo que las dependencias necesarias para ejecutarlo están en el respectivo Pipfile:
````
[[source]]

url = "https://pypi.org/simple"

verify_ssl = true

name = "pypi"

  

[packages]

fastapi = {extras = ["all"], version = "*"}

pika = "*"

grpcio = "*"

grpcio-tools = "*"

  

[dev-packages]

  

[requires]

python_version = "3.10"
````
Para instalar los paquetes se usa el comando ``pipenv sync`` en la raíz del proyecto.

## 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

El proyecto se encuentra desplegado en una instancia EC2 de AWS. Una vez iniciada la instancia es necesario ejecutar el shell script que inicializa todos los servidores. Ejecutar:
````
./reto.sh
````
Hecho esto, ya se puede proceder a enviar peticiones al servidor a través de la dirección IPV4 pública de la instancia.

Para acceder al método de ``list_files`` la sintaxis definida es la siguiente:
````
ip_address:8000/list_files
````
Ej: ``http://107.22.143.11:8000/list_files``

Para acceder al método de ``get_file`` la sintaxis definida es la siguiente:
````
ip_address:8000/get_file?name=nombrearchivo
````
Ej: ``http://107.22.143.11:8000/get_file?name=ex1.txt``

# Referencias:
Fuentes consultadas en el desarrollo del proyecto:
- https://www.rabbitmq.com/tutorials/tutorial-six-python.html
- https://fastapi.tiangolo.com/tutorial/
- https://grpc.io/docs/what-is-grpc/introduction/
- https://betterprogramming.pub/introduction-to-message-queue-with-rabbitmq-python-639e397cb668
#### versión README.md -> 1.0 (2023-Marzo)
