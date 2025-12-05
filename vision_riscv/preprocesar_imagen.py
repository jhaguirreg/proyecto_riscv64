import numpy as np
import cv2
from PIL import Image, ImageOps

def preprocesar(img_raw_pil):
    img_raw = np.array(img_raw_pil)
    
    # Convertir de RGB a Escala de Grises
    img_gray = cv2.cvtColor(img_raw, cv2.COLOR_RGB2GRAY)

    # Aplicar Umbral (Thresholding) e Inversión
    # Usamos cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU para:
    # 1. Binarizar (hacer completamente blanco o negro).
    # 2. Invertir: El número será BLANCO (255) y el fondo NEGRO (0).
    # 3. OTSU: Calcula automáticamente el mejor punto de corte (umbral) para separar el fondo del objeto.
    _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Encontrar Contornos (las fronteras del objeto blanco)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Seleccionar el contorno más grande (asumiendo que es el número y no ruido)
        largest_contour = max(contours, key=cv2.contourArea)

        # Obtener el Bounding Box (x, y, ancho, alto)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Aplicar un margen alrededor del número para no cortarlo y darle espacio
        
        margin = 5
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(img_raw.shape[1], x + w + margin)
        y2 = min(img_raw.shape[0], y + h + margin)

        # Recortar la imagen original en escala de grises con el margen
        cropped_image = img_gray[y1:y2, x1:x2]

    else:
        cropped_image = img_gray # Usar imagen completa como fallback

    return cropped_image

def redimensionar_y_normalizar(imagen):

    cropped_image = preprocesar(imagen)
    print("Imagen recortada al área del número.")

    # Convertir el array de NumPy recortado de nuevo a PIL Image para redimensionar con calidad
    cropped_pil = Image.fromarray(cropped_image)
    # Invertir Colores (si es necesario)
    # Ya hicimos la inversión en el umbral, pero si recortamos de la imagen gris, podría no estar invertida.
    # Para el modelo, el dígito debe ser BLANCO sobre fondo NEGRO.
    if np.mean(cropped_image) > 128:
        final_inverted = ImageOps.invert(cropped_pil)
    else:
        final_inverted = cropped_pil

    # Redimensionar a 28x28 píxeles
    # Esto encoge o estira el número recortado para que encaje perfectamente en 28x28.
    final_28x28 = final_inverted.resize((28, 28), Image.Resampling.LANCZOS)

    # 5. Normalizar y Añadir Dimensión de Batch
    normalized_image = np.array(final_28x28).astype(np.float32) / 255.0 # Normaliza a 0.0 - 1.0
    
    print("Imagen normalizada.")
    return normalized_image



