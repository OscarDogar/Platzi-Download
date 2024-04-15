<div align="center">
  <img src ="https://github.com/OscarDogar/Platzi-Download/assets/60854050/5a57dd93-1138-40d1-9231-c3c029c98bb5"/>
  <h1>Platzi-Download</h1>
</div>

Permite descargar videos de Platzi muchos más rápido. Permite descargar tanto los videos, las lecturas, los subtítulos (si están disponibles) y los recursos de cada una de las clases. 

## 📄Requirements 
- Es **NECESARIO** tener una cuenta de suscripción a Platzi.
- Tener instalado FFmpeg el cual puedes descargar en [https://ffmpeg.org/](https://ffmpeg.org/)
- Tener Google Chrome instalado.
- Descargar el webdriver de selenium con la misma versión de chrome instalada (el cual puedes descargar [aquí](https://chromedriver.chromium.org/downloads)) y colocarlo en la ruta inicial del disco *C*, es decir, *"C:/chromedriver.exe"*
- Instalar requirements.txt
- Cambiar en el archivo .env que se creó al correr el programa por primera vez las variables de entorno que se necesitan:
  1. *EMAIL* = "tuemail@email.com"
  2. *PWD* = "tucontraseña"
  3. *WORDS_TO_REMOVE*(opcional) = word1, word2, word3 (son algunas palabras que se eliminan al momento de descargar una lectura).
 
## 📥Installation

Si lo deseas puedes simplemente descargar el ejecutable del último release el cual puedes encontrar [aquí](https://github.com/OscarDogar/Platzi-Download/releases). 

## 📋Steps

0. Antes que todo lo primero que se deba hacer es cambiar las variables de entorno en el archivo .env que se genera al momento de ejecutar el programa

1. Al iniciar el proceso de descarga, se presenta al usuario la opción de elegir entre dos modalidades: 
   - Descargar un solo video (opción 1).
   - Descargar todos los videos siguientes (opción 2).

2. Opciones.
   - Si el usuario elige la opción 1, se procede a descargar únicamente el video correspondiente a esa URL.
   - Si el usuario selecciona la opción 2, se le solicita ingresar la URL del video desde donde desea comenzar la descarga.

3. Espere hasta que aparezca el mensaje ```Finding videos...```

4. Después, el proceso avanza a la siguiente etapa. El programa navega a la URL proporcionada anteriormente para comenzar la verificación de la disponibilidad de descarga de los videos. Este proceso también se aplica a los subtítulos, recursos y lecturas.

5. Una vez completada la verificación de los videos, el programa empieza a descargar los videos encontrados 1 por 1.

6. Los pasos en que se realiza la descarga es en el siguiente orden:
   - **Descarga de lecturas**: El programa descarga las lecturas al momento de cargar y las guarda en la cartpeta lectures.
   - **Descarga de recursos**: El programa procede a descargar los recursos asociados a los videos, asegurando que todos los materiales auxiliares estén disponibles para el usuario.
   - **Descarga de subtítulos**: Los subtítulos de los videos son descargados, garantizando su disponibilidad para su posterior uso, estos se encuentran dentro de la carpeta del curso, en una carpeta llamada *Subs*.
   - **Descarga de videos**: El programa comienza a descargar los videos y los descarga dentro de la carpeta de videos y dentro de otra carpeta con el nombre del curso.

7. Con todas las descargas completadas, el proceso concluye y los videos, subtítulos y recursos estarán disponibles en una carpeta con el nombre de la clase dentro de la carpeta videos.

## ⚠️Possible failures

* Si hay caídas o desconexiones de internet es posible que se pierda la conexión y no siga descargando o pasando los videos.
* Si se queda quieto y no avanza de una clase.
* Si después de un tiempo no se completa el captcha falla.
* not found en los subtítulos, esto es debido a que no cumplió con algunas validaciones para poderlo descargar.
* All retries failed. es cuando al momento de descargar un video no se pudo descargar algunas de las partes, por lo que se salta este video y sigue al siguiente.
* Si al momento de estar buscando los videos se le da click a otra parte que redireccione a una página distinta, Genera un problema.
* En algunos casos, debido a que el servidor puede presentar problemas no se podra descargar el video por lo que se salta y se pasa al siguiente video. 

## 💕 Sponsor 

- Si este repositorio te ha sido útil o te ha brindado ayuda, te agradecería mucho si pudieras considerar hacer clic en el botón de sponsor. Tu apoyo es lo que impulsa la mejora continua y la creación de nuevos proyectos similares a este. Juntos, podemos seguir haciendo grandes cosas. ¡Gracias por ser parte de esta comunidad!

[Sponsor me <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/60854050/263421335-c7468ed6-7853-42c6-9de9-05be51da1ca2.png" width="20"/>](https://github.com/sponsors/OscarDogar)

## ⭐Star this project 
Recuerda que también puedes ayudarme dándole clic a la estrella en este repositorio en la parte superior [<img width="30" src ="https://github.com/OscarDogar/Platzi-Download/assets/60854050/833aa10d-de1e-472a-8123-3dc1046aa35b"/>](https://github.com/OscarDogar/Platzi-Download/) 


## ✅Result

Una vez completado todo el proceso quedarán los cursos dentro de la carpeta llamada "videos" y dentro estarán otras carpetas 
con el nombre de cada uno de los cursos y dentro de esas carpetas estarán los videos, una carpeta de lectures, una carpeta con los subtítulos y otra con los recursos.

Este sería el resultado dentro de la carpeta *Taller de Inglés Básico sobre Elementos de Trabajo*: 

![image](https://github.com/OscarDogar/Platzi-Download/assets/60854050/d2aa50e8-a7c3-4bb6-8833-7b258e96181c)


## ➕Additional

> [!TIP]
> Si deseas ver los comentarios de las clases deberás iniciar sesión pero puede ser con una cuanta sin suscripción. Puedes utilizar la extensión [Tampermonkey](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo) con el siguiente script:

### [View Platzi Comments](https://gist.githubusercontent.com/OscarDogar/717448f4db972aa01b4cf8b88baab4e2/raw/1641227fb3cd2e104002a9e50353648efd7ff250/ViewPlatziComments.js)


- Para agregar el script a Tampermonkey simplemente es ir a las configuraciones, luego a utilities y despues agregar la url en la parte de abajo.

   ![image](https://github.com/OscarDogar/Platzi-Download/assets/60854050/9a6d2d7b-3b00-4632-b6c8-25f57dfd8a7d)

- Luego aparecerá otra ventana para instalar el script en Tampermonkey. Al final en la pestaña de installed userscripts deberá aparecer el script: 

   ![image](https://github.com/OscarDogar/Platzi-Download/assets/60854050/c3496eaf-dc8f-41a7-8f15-3cb96bf1d801)


## 💡Ejemplo 

Como se puede ver en esta [clase](https://platzi.com/new-home/clases/2069-negocios-data-science/33434-como-crear-empresas-y-culturas-data-driven/), se alcanzan a leer los primeros comentarios de la parte de arriba, pero mientras más se va bajando menos se podrán ver los comentarios [Imagen izquierda]. Ya una vez con el script se podrán ver todos los comentarios sin necesidad de tener una cuenta de pago [Imagen derecha].



<img width="400" src ="https://github.com/OscarDogar/Platzi-Download/assets/60854050/c42d199e-9230-4334-aaf1-10a0d809ef7c"/>
<img width="400" src ="https://github.com/OscarDogar/Platzi-Download/assets/60854050/78322f45-5f97-4f7b-b4c7-96d2155aaefc"/>












