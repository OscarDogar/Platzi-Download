# Platzi-Download

Permite descargar videos de Platzi muchos más rápido. Permite descargar tanto los videos, las lecturas, los subtítulos (si están disponibles) y los recursos de cada una de las clases. 

## Requirements 
- Es **NECESARIO** tener una cuenta de suscripción a Platzi.
- Tener Google Chrome instalado.
- Descargar el webdriver de selenium con la misma versión de chrome instalada y colocarlo en la ruta inicial del disco *C*, es decir, *"C:/chromedriver.exe"*
- Instalar requirements.txt
- Cambiar en el archivo .env que se creó al correr el programa por primera vez las variables de entorno que se necesitan:
  1. *EMAIL* = tuemail@email.com
  2. *PWD* = tucontraseña
  3. *WORDS_TO_REMOVE*(opcional) = word1, word2, word3 (son algunas palabras que se eliminan al momento de descargar una lectura).

## Steps
- Se da la opción para escoger si desea descargar un solo video (1) o todos los videos siguientes (2).
- Se pide la url del video desde donde se quiere empezar a descargar si es con la opción 2 o y si es con la opción 1, solo se descargará ese video.
- Se abre Chrome, lo único para lo que abre es para resolver el Captcha de forma manual que se genera al momento de hacer el login.
- Luego procede a ir al link que se pidió en un principio para empezar a verificar si los videos se pueden descargar, lo mismo para los subtítulos, los recursos y las lecturas.
- Una vez termine de analizar los videos, automáticamente cierra la ventana.
- Una vez cerrado la ventana empieza a descargar primero los recursos, luego los subtítulos, luego los videos, y por ultimo los subtítulos.


## Result

Una vez completado todo el proceso quedarán los cursos dentro de la carpeta llamada "videos" y dentro estarán otras carpetas 
con el nombre de cada uno de los cursos y dentro de esas carpetas estarán los videos, una carpeta de lectures, una carpeta con los subtítulos y otra con los recursos.



