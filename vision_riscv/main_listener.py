#!/usr/bin/env python3
# Archivo: /opt/vision_riscv/main_listener.py

import sys
import gpiod # Importación CORRECTA de la librería instalada
import gpiod # Importación CORRECTA de la librería instalada
import time
import cargar_datos
import modelo_predictivo
import numero_a_morse
import preprocesar_imagen
import tomar_captura

# --- CONFIGURACIÓN DE PINES Y PARÁMETROS ---
CHIP_NAME = 'gpiochip0' 
BUTTON_LINE_OFFSET = 32 # <--- OFFSET DEL BOTÓN CONFIRMADO
BUZZER_LINE_OFFSET = 33 # <--- REEMPLAZAR con el offset REAL del Buzzer.

# Tiempos de Morse
DOT_DURATION = 0.1       # Duración del Punto
DASH_DURATION = 0.5      # Duración de la Raya
SYMBOL_PAUSE = 0.3       # Pausa entre símbolos
REPETITION_PAUSE = 1.0   # Pausa entre repeticiones de la secuencia (REQ-F06)

# Variables globales para manejar los recursos GPIO de forma segura
buzzer_line = None 
buzzer_chip = None
button_line = None
button_chip = None


# --- FUNCIONES AUXILIARES DE CONTROL ---

def initialize_gpio_resources():
    """ Inicializa los chips y las líneas de E/S. """
    global buzzer_chip, buzzer_line, button_chip, button_line
    
    # 1. Configuración del Buzzer (Salida)
    buzzer_chip = gpiod.Chip(CHIP_NAME)
    buzzer_line = buzzer_chip.get_line(BUZZER_LINE_OFFSET)
    # Solicita la línea como SALIDA (OUTPUT)
    buzzer_line.request(consumer='buzzer_output', type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    
    # 2. Configuración del Botón (Entrada con Interrupción)
    button_chip = gpiod.Chip(CHIP_NAME)
    button_line = button_chip.get_line(BUTTON_LINE_OFFSET)
    # Solicita la línea para detectar flanco de bajada (al presionar)
    button_line.request(consumer='vision_riscv_btn', 
                        type=gpiod.LINE_REQ_EV_FALLING_EDGE, 
                        flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
    
    print(f"Buzzer y Botón inicializados correctamente.")
    
    if buzzer_line is None:
        raise Exception(f"La línea del buzzer (Offset 33) no fue inicializada correctamente. El pin está en uso o no existe.")
    if button_line is None:
        raise Exception(f"La línea del button (Offset 32) no fue inicializada correctamente. El pin está en uso o no existe.")


def release_gpio_resources():
    global buzzer_chip, buzzer_line, button_chip, button_line

    """ Libera todos los recursos GPIO solicitados (función 'cleanup' de gpiod). """
    if button_line and button_line.is_requested():
         button_line.release()
    if button_chip:
         button_chip.close()
    if buzzer_line and buzzer_line.is_requested():
         buzzer_line.release()
    if buzzer_chip:
         buzzer_chip.close()
    print("Recursos GPIO liberados. Servicio detenido.")


def emit_morse_symbol(symbol_type):
    global buzzer_chip, buzzer_line, button_chip, button_line

    """ Emite un punto o una raya con la duración precisa (REQ-F05). """
    duration = DOT_DURATION if symbol_type == '.' else DASH_DURATION
    
    # 1. Encender (Pin HIGH)
    buzzer_line.set_value(1) 
    time.sleep(duration)
    
    # 2. Apagar (Pin LOW)
    buzzer_line.set_value(0)
    
    # 3. Pausa entre símbolos
    time.sleep(SYMBOL_PAUSE)

# --- 1. FUNCIÓN PRINCIPAL DE LÓGICA DEL PROYECTO (Simulación REQ-F01 a REQ-F06) ---

def ejecutar_ciclo_completo(pesos):
    global buzzer_chip, buzzer_line, button_chip, button_line

    ruta_de_la_foto = tomar_captura.capturar_y_guardar_temp()

    imagen = tomar_captura.cargar_imagen_pil(ruta_de_la_foto)

    if imagen is None:
        print("ERROR: No se pudo cargar la imagen capturada. Abortando ciclo.")
        return
    imagen_preprocesada = preprocesar_imagen.redimensionar_y_normalizar(imagen)
    digito,_ = modelo_predictivo.predict(imagen_preprocesada, pesos)

    print(f"Número detectado: {digito}")
    secuencia_morse = numero_a_morse.conv_numero_a_morse(digito)
    
    # --- EMISIÓN SONORA Y REPETICIÓN (REQ-F05, REQ-F06) ---
    for i in range(3): # Repetir 3 veces (REQ-F06)
        
        # Emitir la secuencia 
        for symbol in secuencia_morse:
            emit_morse_symbol(symbol)
            
        if i < 2:
            # Pausa de 1 s entre repeticiones (REQ-F06)
            time.sleep(REPETITION_PAUSE) 

    print("Ciclo completado. Esperando nueva pulsación...")

def main():
    global buzzer_chip, buzzer_line, button_chip, button_line

    print("--- Sistema de Visión RISC-V: Iniciando Servicio Daemon ---")

    try:
        pesos = cargar_datos.cargar_pesos_npy()
        initialize_gpio_resources()
        
        print(f"Inicializado correctamente. Esperando pulsación del botón...")
        
        # Bucle principal para escuchar eventos
        while True:
            # event_wait espera a que ocurra un evento de interrupción (bajo consumo de CPU)
            events = button_line.event_wait(sec=60)
            if events:
                event = button_line.event_read()
                # Reacciona solo al flanco de bajada (al presionar el botón)
                if event.type == gpiod.LineEvent.FALLING_EDGE:
                    ejecutar_ciclo_completo(pesos) # Inicia el ciclo del proyecto
            
    except Exception as e:
        print(f"*** FALLO CRÍTICO DETECTADO. Systemd Reiniciará ***")
        print(f"Error: {e}")
        sys.exit(1) # Provoca la salida para que systemd active Restart=always
        
    finally:
        release_gpio_resources()


if __name__ == "__main__":
    main()
