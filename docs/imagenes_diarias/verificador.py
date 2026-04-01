import os

def verificar_nombres_archivos(prefijos=("2025", "2026"), longitud_esperada=60):
    # Detectar la ruta donde se está ejecutando el script
    ruta_principal = os.path.dirname(os.path.abspath(__file__))
    
    contadores = {
        "correctos": 0,
        "ignorados_por_extension": 0
    }
    # Ahora guardaremos tuplas con la ruta y el motivo del error
    archivos_incorrectos = []

    prefijos_str = " o ".join(prefijos)
    print(f"Iniciando verificación (Prefijos: {prefijos_str} | Longitud exacta: {longitud_esperada} caracteres)...\n")

    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_principal):
        
        if '.vscode' in carpeta_actual:
            continue

        for nombre_archivo in archivos:
            if nombre_archivo == os.path.basename(__file__):
                continue

            if not nombre_archivo.lower().endswith(('.jpg', '.jpeg', '.mp4')):
                contadores["ignorados_por_extension"] += 1
                continue

            # Separar las validaciones lógicas
            empieza_bien = nombre_archivo.startswith(prefijos)
            longitud_correcta = len(nombre_archivo) == longitud_esperada

            # Si cumple ambas reglas, es correcto
            if empieza_bien and longitud_correcta:
                contadores["correctos"] += 1
            else:
                # Si falla una o ambas, determinamos exactamente por qué
                ruta_completa = os.path.join(carpeta_actual, nombre_archivo)
                causas = []
                
                if not empieza_bien:
                    causas.append(f"No inicia con {prefijos_str}")
                if not longitud_correcta:
                    causas.append(f"Tiene {len(nombre_archivo)} caracteres")
                
                # Unimos las causas encontradas y las guardamos
                motivo_error = " y ".join(causas)
                archivos_incorrectos.append((ruta_completa, motivo_error))

    # -----------------------------------------
    # Reporte final en consola
    # -----------------------------------------
    print("-" * 60)
    print("RESUMEN DE VERIFICACIÓN")
    print("-" * 60)
    print(f"Archivos válidos encontrados: {contadores['correctos']}")
    
    if archivos_incorrectos:
        print(f"\n¡Atención! Se encontraron {len(archivos_incorrectos)} archivo(s) con errores:")
        for ruta, motivo in archivos_incorrectos:
            # Imprime la ruta y al final entre corchetes la causa exacta del error
            print(f" ❌ {ruta} -> [Error: {motivo}]")
    else:
        print(f"\n✅ Todo en orden. Todos los archivos cumplen con los prefijos y la longitud de {longitud_esperada} caracteres.")

if __name__ == '__main__':
    # Pasamos la tupla de años y el número exacto de caracteres esperados
    verificar_nombres_archivos(("2025", "2026"), 64)