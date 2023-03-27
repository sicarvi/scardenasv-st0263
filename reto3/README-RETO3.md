# st0263-231 Tópicos Especiales en Telemática.

## Estudiante: Simón Cárdenas Villada, scardenasv@eafit.edu.co

## Profesor: Edwin Nelson Montoya Múnera, emontoya@eafit.edu.co

# Reto 3
## 1. Breve descripción de la actividad

### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Se desarrolló un despliegue de CMS Wordpress escalable, haciendo uso de una base datos relacional y un sistema de archivos distribuido NFS para la persistencia de datos, y un servidor de balanceo de carga que implementa NGINX. Todo esto se hizo a través de contenedores docker para facilitar la instalación y gestión de las distintas aplicaciones.

## 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

**Esta fue la arquitectura implementada:** 

![imagen arq](https://github.com/sicarvi/scardenasv-st0263/blob/master/reto3/Pasted%20image%2020230326161637.png?raw=true)

El despliegue del sistema se hizo en nube con máquinas virtuales de GCP, además el dominio cuenta con un certificado SSL asociado, por lo que el acceso al Wordpress esta soportado sobre el protocolo HTTPS.

## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerías, paquetes, etc, con sus números de versiones.
- Este proyecto fue desarrollado en Ubuntu **22.04**.
- Se hizo uso de Docker para generar los contenedores sobre los que corren cada aplicación.
- La certificación SSL se obtuvo de forma gratuita a través de CertBot.

### Configuración General
En todas las máquinas que se vayan a utilizar es necesario contar con los paquetes más recientes, además de tener docker instalado y configurado. Esto se puede lograr a través de los siguientes comandos:
```bash
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker <usuario>
```

### Configuración WordPress
Para la instalación de WordPress es necesario crear el archivo del `docker compose` que se usará para general el contenedor. Debe crearse una carpeta en la ruta de inicio (Ej: `/home/user/wordpress`) y allí crear un archivo llamado `docker-compose.yml` que contenga lo siguiente:
```yml
version: '3.1'
services:
  wordpress:
    container_name: wordpress
    image: wordpress
    ports:
      - 80:80      
    restart: always
    environment:
      WORDPRESS_DB_HOST: <ip_privada_bd>
      WORDPRESS_DB_USER: exampleuser
      WORDPRESS_DB_PASSWORD: examplepass
      WORDPRESS_DB_NAME: exampledb
    volumes:
      - /mnt/wordpress:/var/www/html
```
El campo de `WORDPRESS_DB_HOST` corresponde a la IP privada de la maquina en donde este corriendo la base de datos, más adelante la configuraremos. 
Esta configuración debe hacerse en todas la VM que vayan a tener el WordPress corriendo, para asegurar que escalen en forma conjunta.
Una vez se tengan los pasos anteriores listos, crear y ejecutar el contenedor de docker por medio del comando:
```bash
docker-compose up --build -d
```


### Configuración base de datos (MySQL)
Crear un directorio en la ruta de inicio de la misma forma que se hizo para el WordPress. Allí irá el archivo `docker-compose.yml` con la configuración de MySQL:
```yml
version: '3.1'
services:
  db:
    image: mysql:5.7
    restart: always
    ports:
      - 3306:3306 
    environment:
      MYSQL_DATABASE: exampledb
      MYSQL_USER: exampleuser
      MYSQL_PASSWORD: examplepass
      MYSQL_RANDOM_ROOT_PASSWORD: '1'
    volumes:
      - db:/var/lib/mysql
volumes:
  db:
```
Además de esto se debe crear una regla de entrada en el firewall para que permita la entrada de tráfico TCP por el puerto `3306`. En GCP se hace a través de Firewall>Crear regla de firewall. Recuerde definir una etiqueta de red para poder aplicarla en la VM, ejemplo:

![imagen firewall](https://github.com/sicarvi/scardenasv-st0263/blob/master/reto3/Pasted%20image%2020230326172352.png?raw=true)

Una vez se tengan los pasos anteriores listos, crear y ejecutar el contenedor de docker por medio del comando:
```bash
docker-compose up --build -d
```

### Configuración NFS
Para configurar el sistema de archivos distribuidos es necesario realizarlo tanto en el *host* como en los *clientes*. En nuestro caso el *host* será una instancia en GCP que contiene la configuración de servidor NFS, y los *clientes* serán las instancias que estén corriendo el WordPress.
Primero hay que instalar los paquetes necesarios en cada máquina:
*Host*
```bash
sudo apt install nfs-kernel-server
```
*Cliente*
```bash
sudo apt install nfs-common
```
Luego crear el directorio que va a ser compartido y actualizar sus permisos:
*Host*
```bash
sudo mkdir /var/nfs/general -p
sudo chown nobody:nogroup /var/nfs/general
```
Una vez hecho esto se debe abrir el archivo de configuraicones NFS con privilegios root:
*Host*
```bash
sudo nano /etc/exports
```
Añadir lo siguiente:
```
/var/nfs/general        10.128.0.0/16(rw,sync,no_root_squash,no_subtree_check)
```
Esta configuración debe de hacerse para todos los directorios que deseen compartirse y la IP a ingresar es la dirección de la máquina autorizada para conectarse al fichero compartido, pero también puede ponerse la IP privada resumida como en el ejemplo anterior, que permitirá la conexión de un rango de IPs privadas. Para hacer efectiva la configuración  ingresar el comando:
*Host*
```bash
sudo systemctl restart nfs-kernel-server
```
**Nota:** Es importante verificar que el firewall del *Host* cuente con una regla que permita el tráfico por el puerto `2049`.
Ahora se debe configurar los puntos de montaje en en los clientes. Para esto se deben ejecutar los siguientes comandos:

*Cliente*
```bash
sudo mkdir -p /mnt/wordpress
sudo mount host_ip:/var/nfs/general /mnt/wordpress
```
Recuerde reemplazar `host_ip` por la IP privada del *host*.

### Configuración NGINX para balanceo de carga
Instale los paquetes necesarios a través de los siguientes comandos:
```bash
sudo add-apt-repository ppa:certbot/certbot
sudo apt install letsencrypt -y
sudo apt install nginx -y
```
Luego acceda al archivo de configuración de NGINX a través de `sudo vim /etc/nginx/nginx.conf` e ingrese la siguiente información:
```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections  1024;  ## Default: 1024
}
http {
    server {
        listen  80 default_server;
        server_name _;
        location ~ /\.well-known/acme-challenge/ {
            allow all;
            root /var/www/letsencrypt;
            try_files $uri = 404;
            break;
        }
    }
}
```
Guarde el archivo y ejecute los siguientes comandos para aplicar los cambios:
```bash
sudo mkdir -p /var/www/letsencrypt
sudo nginx -t
sudo service nginx reload
```
Luego hay que ejecutar CertBot para solicitar los certificados SSL para su dominio específico:
```bash
sudo letsencrypt certonly -a webroot --webroot-path=/var/www/letsencrypt -m email@address --agree-tos -d sudominio.tk
```
Recuerde reemplazar su correo electrónico y nombre de dominio donde corresponde.

Ahora debe crearse una carpeta en la ruta de inicio (Ej: `/home/user/docker_nginx`) y allí crear los siguientes archivos de configuración: 
`docker-compose.yml` :
```yml
version: '3.1'
services:
  nginx:
    container_name: nginx
    image: nginx
    volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl
    - ./ssl.conf:/etc/nginx/ssl.conf
    ports:
    - 80:80      
    - 443:443
    restart: always
```
`nginx.conf` :
```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
  worker_connections  1024;  ## Default: 1024
}
http {

upstream backend {
        server <ip_wordpress1>;
        server <ip_wordpress2;
    }

server {
  listen 80;
  listen [::]:80;

  server_name _;
  rewrite ^ https://$host$request_uri permanent;
}

server {
  listen 443 ssl http2 default_server;
  listen [::]:443 ssl http2 default_server;

  server_name _;

  # enable subfolder method reverse proxy confs
  #include /config/nginx/proxy-confs/*.subfolder.conf;

  # all ssl related config moved to ssl.conf
  include /etc/nginx/ssl.conf;

  client_max_body_size 0;
  location / {
    proxy_pass http://backend;
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Server $host;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
}
```
Recuerde reemplazar la dirección IP privada de sus instancias WordPress donde corresponde.
`ssl.conf` :
```
## Version 2018/05/31 - Changelog: https://github.com/linuxserver/docker-letsencrypt/commits/master/root/defaults/ssl.conf

# session settings
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# Diffie-Hellman parameter for DHE cipher suites
# ssl_dhparam /etc/nginx/ssl/ssl-dhparams.pem;

# ssl certs
ssl_certificate /etc/nginx/ssl/fullchain.pem;
ssl_certificate_key /etc/nginx/ssl/privkey.pem;

# protocols
ssl_protocols TLSv1.1 TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA>

# HSTS, remove # from the line below to enable HSTS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;

# Optional additional headers
#add_header Content-Security-Policy "upgrade-insecure-requests";
#add_header X-Frame-Options "SAMEORIGIN" always;
#add_header X-XSS-Protection "1; mode=block" always;
#add_header X-Content-Type-Options "nosniff" always;
#add_header X-UA-Compatible "IE=Edge" always;
#add_header Cache-Control "no-transform" always;
#add_header Referrer-Policy "same-origin" always;
```


Ahora cree una carpeta adentro de este directorio con `mkdir ssl` y ejecute el siguiente comando para copiar los archivos de configuracion SSL:
```bash
cp /etc/letsencrypt/live/sudominio.tk/* /home/user/wordpress/ssl/
```
Recuerde reemplazar el nombre de su dominio y usuario ubuntu en donde corresponda.

Verifique que NGINX no se esté ejecutando, y deténgalo en caso de ser necesario con los siguientes comandos:
```bash
ps ax | grep nginx

sudo systemctl disable nginx
sudo systemctl stop nginx
```
Una vez se tengan los pasos anteriores listos, crear y ejecutar el contenedor de docker por medio del comando:
```bash
docker-compose up --build -d
```
Recuerde inscribir en los registros de su DNS la dirección IP pública del servidor NGINX para que pueda acceder por medio de internet al dominio.

## 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus números de versiones.

Así luciría la consola de Google Cloud Platform una vez se tengan todas las VM desplegadas:

![imagen gcp](https://github.com/sicarvi/scardenasv-st0263/blob/master/reto3/Pasted%20image%2020230326185126.png?raw=true)

Y el sitio web funcionando:

![imagen web](https://github.com/sicarvi/scardenasv-st0263/blob/master/reto3/Pasted%20image%2020230326185409.png?raw=true)
# Referencias:
Fuentes consultadas en el desarrollo del proyecto:
- https://github.com/st0263eafit/st0263-231/tree/main/docker-nginx-wordpress-ssl-letsencrypt
- https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04-es
- https://hub.docker.com/_/nginx
- https://hub.docker.com/_/mysql
#### versión README-RETO3.md -> 1.0 (2023-Marzo)
