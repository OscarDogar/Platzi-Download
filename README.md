# Platzi-Download

Permite descargar videos de platzi muchos más rápido. Permite descargar tanto los videos, las lecturas, los subtítulos (si están disponibles) y los recursos de cada una de las clases. 

## Requirements 
- Es **NECESARIO** tener una cuenta de suscripción a Platzi.
- Tener Google Chrome instalado.
- Descargar el webdriver de selenium para Chrome y colocarlo en la ruta inicial del disco C:, es decir, *"C:/chromedriver.exe"*
- Instalar requirements.txt
- Crear un archivo .env para agregar algunas variables de entorno que se necesitan:
  1. *EMAIL* = tuemail@email.com
  2. *PWD* = tucontraseña
  3. *START_DOWNLOAD_URL* = el link del primer video del curso que quieras descargar.
  4. *WORDS_TO_REMOVE*(opcional) : son algunas palabras que se eliminar al momento de descargar una lectura.

## Steps
- Se da la opción para escoger si desea descargar un solo video (1) o todos los videos siguientes a partir de *START_DOWNLOAD_URL* (2).
- Se abre Chrome, lo único para lo que abre es para resolver el Captcha de forma manual que se genera al momento de hacer el login.
- Luego procede a ir al link *START_DOWNLOAD_URL* para empezar a verificar si los videos se pueden descargar, lo mismo para los subtítulos, los recursos y las lecturas.
- Una vez validado todo empieza a descargar primero los recursos, luego los subtítulos, luego los videos, y por ultimo los subtítulos.


## Result

Una vez completado todo el proceso quedarán los cursos dentro de la carpeta llamada "videos" y dentro estarán otras carpetas 
con el nombre de cada uno de los cursos y dentro de esas carpetas estarán los videos, una carpeta de lectures, una carpeta con los subtítulos y otra con los recursos.



