# PROYECTO RISCV64: Servicio de Detección y Morse

Este repositorio contiene el código fuente para un sistema de detección (basado en el modelo MNIST) y conversión a código Morse, diseñado para ejecutarse como un servicio del sistema en una arquitectura RISC-V 64-bit (riscv64).

## Estructura del Proyecto
La estructura del repositorio está diseñada para ser instalada limpiamente en el sistema operativo:

* **`vision_riscv/`**: Contiene todo el código fuente de la aplicación, que será copiado a `/opt/vision_riscv`.
    * `pesos/`: Directorio que contiene los archivos de pesos del modelo predictivo.
    * `cargar_datos.py`: Script para la carga de los pesos del modelo que están en `.npy`.
    * `main_listener.py`: Script de inicio principal del servicio. Contiene la lógica principal y configuración de los GPIO.
    * `modelo_predictivo.py`: Contiene la definición y lógica del modelo de Machine Learning.
    * `numero_a_morse.py`: Utilidad para convertir el resultado numérico de la predicción a código Morse.
    * `preprocesar_imagen.py`: Script para preparar la imagen de entrada antes de ser alimentada al modelo.
    * `tomar_captura.py`: Utilidad para adquirir la imagen o captura de datos.
* **`vision_riscv.service`**: El archivo de unidad de Systemd necesario para ejecutar la aplicación como un servicio persistente en segundo plano (copiado a `/etc/systemd/system/`).
* **`install.sh`**: Script de instalación para automatizar la colocación de archivos en directorios del sistema.

## 1. Instalación del Servicio

La instalación está automatizada mediante el script `install.sh`. Este script copia los archivos de la aplicación a `/opt` y el archivo de servicio a `/etc/systemd/system/`.

### 1.1. Pasos de Instalación

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_del_repositorio>
    cd PROYECTO_RISCV64
    ```

2.  **Dar Permisos de Ejecución al Script:**
    ```bash
    chmod +x install.sh
    ```

3.  **Ejecutar la Instalación (Requiere `sudo`):**
    ```bash
    sudo ./install.sh
    ```

El script realizará las siguientes acciones automáticamente:
* Copia el directorio `vision_riscv` a **/opt/**.
* Copia el archivo `vision_riscv.service` a **/etc/systemd/system/**.
* Ejecuta `sudo systemctl daemon-reload`.
* **Habilita** e **Inicia** el servicio.

***

## 2. Gestión del Servicio (Systemd)

Una vez instalado, el servicio se llama `vision_riscv.service` y se gestiona con el comando `systemctl`.

| Comando | Descripción |
| :--- | :--- |
| `sudo systemctl status vision_riscv.service` | **Verifica el estado** actual del servicio (activo, inactivo, fallando). |
| `sudo systemctl start vision_riscv.service` | Inicia el servicio. |
| `sudo systemctl stop vision_riscv.service` | Detiene el servicio. |
| `sudo systemctl restart vision_riscv.service` | Reinicia el servicio (útil después de hacer cambios en el código o en el archivo de servicio). |
| `sudo systemctl enable vision_riscv.service` | Asegura que el servicio se inicie automáticamente en cada arranque del sistema. |
| `sudo systemctl disable vision_riscv.service` | Deshabilita el inicio automático del servicio. |

### 2.1. Recarga de Configuración (Importante)

Si editas el archivo de servicio **`/etc/systemd/system/vision_riscv.service`** directamente, debes ejecutar el siguiente comando para que Systemd reconozca los cambios antes de reiniciar el servicio:

```bash
sudo systemctl daemon-reload
```

Luego, reinicia el servicio para aplicar la nueva configuración:
```bash
sudo systemctl restart vision_riscv.service
```

## 3. Detalles del Servicio (`vision_riscv.service`)

El archivo de servicio está configurado para garantizar la alta disponibilidad y la correcta ejecución en el entorno RISC-V.

| Parámetro    | Valor y Propósito                                                                                                              |
|--------------|----------------------------------------------------------------------------------------------------------------------------------|
| **Description** | Servicio de Detección MNIST RISC-V y Morse                                                                                      |
| **After**        | `network.target` (Asegura que la red esté disponible antes de iniciar).                                                          |
| **ExecStart**    | `/usr/bin/python3 /opt/vision_riscv/main_listener.py`. Esta es la ruta crítica de ejecución.                                     |
| **User**         | `root` (Necesario para acceder a recursos del sistema, como pines GPIO del kernel).                                             |
| **Restart**      | `always` (Asegura que el servicio se reinicie automáticamente si falla).                                                         |
| **RestartSec**   | `2` (Espera 2 segundos antes de intentar reiniciar después de un fallo).                                                         |
| **WantedBy**     | `multi-user.target` (Inicia el servicio en el modo de operación normal del sistema).                                             |


## 4. Desinstalación del Servicio

Para eliminar todos los archivos instalados del sistema y deshabilitar el servicio, utiliza el mismo script de instalación con el argumento uninstall:
```bash
sudo ./install.sh uninstall
```

