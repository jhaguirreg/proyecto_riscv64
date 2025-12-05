def conv_numero_a_morse(numero) -> str:

    # Diccionario de mapeo de dígitos a Código Morse
    # El Código Morse para los dígitos es universal.
    MAPEO_MORSE = {
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        '0': '-----'
    }
    
    # Asegurarse de que la entrada sea una cadena de dígitos
    try:
        digito = str(numero)
    except Exception:
        print("Error: La entrada debe ser convertible a una cadena de dígitos.")
        return ""

    if digito in MAPEO_MORSE:
        # Mapear el dígito a su código morse y agregarlo a la lista
        codigo_morse_resultado = MAPEO_MORSE[digito]
    else:
        # Manejar cualquier carácter que no sea un dígito (ej: un espacio si se incluyó)
        print(f"Advertencia: El carácter '{digito}' no es un dígito y será ignorado.")
        codigo_morse_resultado = ""
    
    return codigo_morse_resultado