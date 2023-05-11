# ST0263-4529
## Estudiante
- Simón Cárdenas Villada, scardenasv@eafit.edu.co.
## Docente:
- Edwin Nelson Montoya Munera, emontoya@eafit.brightspace.com

# Reto 5-2
## Descripción del proyecto
## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
En este laboratorio se usó un Cluster AWS EMR para practicar la gestión de archivos en HDFS y S3.
## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)  
Todos los requisitos solicitados fueron completados. 

## 2. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus números de versiones.
- Se creó el cluster por medio de la clonación de una plantilla previamente establecida
- Se creó un bucket S3 para el almacenamiento de archivos
- Se creó a través de la interfaz online de AWS y se uso SSH para conectarse al nodo maestro desde la consola Powershell de Windows, con el fin de realizar las operaciones sobre el HDFS.
- También se usó la interfaz de aplicación de HUE para interactuar con los archivos del cluster.

## 3. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.  

Primero se creó un bucket S3 con acceso público de acuerdo a las instrucciones dadas:
![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510211333.png?raw=true)
Para lograr esto se quitó la protección de acceso público que viene por defecto, y además es necesario añadir la siguiente configuración en las políticas del bucket:
```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::st0263scardenasv"
        }
    ]
}
```
Una vez hecho esto se pueden cargar los archivos del dataset deseado y cualquier usuario con la URL podrá ver el contenido:
![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212237.png?raw=true)

### Operaciones realizadas en el HDFS:

Copiar archivos dataset a Hadoop por medio de SCP:

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510211950.png?raw=true)

Copiar archivos locales hacia HDFS:

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212149.png?raw=true)

Copiar archivos de S3 a HDFS:

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212405.png?raw=true)

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212422.png?raw=true)

Copia recursiva de datos:

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212506.png?raw=true)

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212514.png?raw=true)

Explorador de archivos en Hadoop:

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212608.png?raw=true)

Creación de directorio:

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212656.png?raw=true)

Subir archivo:

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212717.png?raw=true)

Ver contenido del archivo:

![img](https://github.com/sicarvi/scardenasv-st0263/blob/master/bigdata/5-2/Pasted%20image%2020230510212731.png?raw=true)

## Referencias
* [Github de la materia](https://github.com/st0263eafit/st0263-231/blob/main/bigdata/lab5-1-aws-emr.txt)  
* [Documentación bucket S3](https://repost.aws/es/knowledge-center/read-access-objects-s3-bucket)
* [Uso de SCP](https://learn.microsoft.com/es-es/azure/virtual-machines/copy-files-to-vm-using-scp)
