import cv2
import time
import tempfile
import os
from PIL import Image

def capturar_y_guardar_temp() -> str:
    
    camera_index = 0
    nombre_archivo = "captura.jpg"

    # Definir la ruta temporal usando tempfile.gettempdir()
    # Esta función siempre devuelve la ubicación temporal estándar del OS.
    directorio_temp = tempfile.gettempdir() 
    
    # Construir la ruta completa: /tmp/nombre_archivo.jpg
    ruta_completa = os.path.join(directorio_temp, nombre_archivo)

    # Inicializar la captura de video
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"ERROR: No se pudo acceder a la cámara.")
        return ""

    # Esperar y capturar el fotograma
    cap.read() 
    time.sleep(1)
    ret, frame = cap.read()

    # Liberar el recurso de la cámara
    cap.release()

    if ret:
        # Guardar la imagen
        cv2.imwrite(ruta_completa, frame)
        return ruta_completa
    else:
        print("ERROR: No se pudo capturar el fotograma.")
        return ""

def cargar_imagen_pil(ruta_imagen: str):
    try:
        imagen = Image.open(ruta_imagen)
        return imagen
    except Exception as e:
        print(f"ERROR: No se pudo cargar la imagen desde {ruta_imagen}. Detalles: {e}")
        return None