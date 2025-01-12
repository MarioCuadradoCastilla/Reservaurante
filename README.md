pip install -r requirements.txt
python -m venv .venv
source .venv/bin/activate     # En Mac o Linux
.venv\Scripts\activate  win
repository: github:https://github.com/MarioCuadradoCastilla/Reservaurante/tree/master
python version: 3.12.8
especificaciones:
    -las imagenes de la base de datos, están dentro del directorio de la base de datos ya que la idea es tratarlas como datos
    -los Datos de demo y el archivo ejecutable para cargarlos, se encuentran en la carpeta Data/DemoData
    -el archivo que ejecuta la aplicación es el main.py que se encuentra en la raiz del proyecto
    -Las pruebas realizadas están en el directorio test
    -las imagenes que no correspoden a las de los restaurnntes de la base de datos se encuentran en la carpeta img
    -PARA WINDOWS