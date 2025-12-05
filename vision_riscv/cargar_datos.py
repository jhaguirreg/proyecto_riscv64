import os
import numpy as np

# Esta función carga múltiples archivos .npy desde un directorio específico.
def cargar_pesos_npy() -> list:
    
    # Ruta base donde se encuentran los archivos .npy.
    directorio_base = "/opt/vision_riscv/pesos"
    num_archivos = 10

    # Lista para almacenar los arrays cargados.
    pesos = []
    
    # Verifica que el directorio exista.
    if not os.path.isdir(directorio_base):
        return pesos # Retorna lista vacía

    print(f"Iniciando carga de archivos.")

    # Itera sobre el rango y construye el nombre del archivo
    for i in range(num_archivos):
        
        # Construye la ruta completa, e.g., /opt/vision_riscv/pesos/peso_0.npy
        nombre_archivo = f"peso_{i}.npy"
        ruta_completa = os.path.join(directorio_base, nombre_archivo)
        
        try:
            # np.load() carga el array de NumPy.
            array_cargado = np.load(ruta_completa)
            
            # Agrega el array cargado a la lista.
            pesos.append(array_cargado)
            
        except FileNotFoundError:
            print(f"ERROR: Archivo no encontrado en la ruta: {ruta_completa}")
            # Si un archivo falta en la secuencia, se detiene la carga
            return [] 
            
        except Exception as e:
            print(f"ERROR al cargar {ruta_completa}: {e}")
            return []

    print(f"Carga de archivos finalizada.")
    return pesos