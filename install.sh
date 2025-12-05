#!/bin/bash

# --- Variables de configuración ---
# Directorio local de la aplicación
APP_LOCAL_DIR="vision_riscv"
# Nombre del archivo de servicio local
SERVICE_LOCAL_FILE="vision_riscv.service"

# Directorios de destino en el sistema
INSTALL_DIR="/opt/${APP_LOCAL_DIR}"
SYSTEMD_PATH="/etc/systemd/system"

# --- Funciones de utilidad ---

# Función para verificar privilegios de root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo "Error: Este script debe ejecutarse con 'sudo'. Por favor, use 'sudo ./install.sh'"
        exit 1
    fi
}

# Función de limpieza (Desinstalación)
uninstall() {
    echo "Iniciando la desinstalación de ${APP_LOCAL_DIR}..."
    
    # 1. Detener y deshabilitar el servicio
    if systemctl is-active --quiet "$SERVICE_LOCAL_FILE"; then
        echo "   -> Deteniendo servicio..."
        systemctl stop "$SERVICE_LOCAL_FILE"
    fi
    if systemctl is-enabled --quiet "$SERVICE_LOCAL_FILE"; then
        echo "   -> Deshabilitando servicio..."
        systemctl disable "$SERVICE_LOCAL_FILE"
    fi
    
    # 2. Eliminar archivos
    echo "   -> Eliminando archivo de servicio: $SYSTEMD_PATH/$SERVICE_LOCAL_FILE"
    rm -f "$SYSTEMD_PATH/$SERVICE_LOCAL_FILE"
    
    echo "   -> Eliminando directorio de la aplicación: $INSTALL_DIR"
    rm -rf "$INSTALL_DIR"
    
    # 3. Recargar el demonio de systemd
    systemctl daemon-reload &> /dev/null
    
    echo "Desinstalación de ${APP_LOCAL_DIR} completa."
    exit 0
}

# --- Lógica principal de instalación ---

install_app() {
    echo "Iniciando la instalación de ${APP_LOCAL_DIR}..."

    # 1. Copiar el directorio de la aplicación a /opt
    if [ -d "./$APP_LOCAL_DIR" ]; then
        echo "   -> Copiando directorio de la aplicación a $INSTALL_DIR..."
        cp -r "./$APP_LOCAL_DIR" "$INSTALL_DIR"
    else
        echo "Error fatal: El directorio './$APP_LOCAL_DIR' no se encontró. ¿Está ejecutando el script desde la raíz del repositorio?"
        exit 1
    fi

    # 2. Copiar el archivo de unidad de systemd a /etc/systemd/system
    if [ -f "./$SERVICE_LOCAL_FILE" ]; then
        echo "   -> Instalando el archivo de servicio en $SYSTEMD_PATH/$SERVICE_LOCAL_FILE..."
        cp "./$SERVICE_LOCAL_FILE" "$SYSTEMD_PATH/"
    else
        echo "Error fatal: El archivo de servicio './$SERVICE_LOCAL_FILE' no se encontró. Abortando instalación del servicio."
        exit 1
    fi

    # 3. Recargar la configuración de systemd
    echo "Recargando la configuración del demonio de systemd..."
    systemctl daemon-reload

    # 4. Habilitar y arrancar el servicio
    echo "   -> Habilitando y arrancando el servicio $SERVICE_LOCAL_FILE..."
    systemctl enable "$SERVICE_LOCAL_FILE"
    systemctl start "$SERVICE_LOCAL_FILE"

    echo "Instalación de ${APP_LOCAL_DIR} completa."
    echo "Para verificar el estado del servicio: sudo systemctl status $SERVICE_LOCAL_FILE"
}

# --- Manejo de argumentos y ejecución ---

# Comprueba si el usuario quiere desinstalar
if [ "$1" == "uninstall" ]; then
    check_root
    uninstall
fi

# Inicia la instalación
check_root
install_app