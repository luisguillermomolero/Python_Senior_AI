import subprocess
import sys
import time

# Constantes
SEPARADOR = "─" * 50
PYTHON_VERSION_MIN = (3, 8)

# Lista de dependencias necesarias para el proyecto
# Versiones compatibles para evitar errores de bcrypt con passlib
dependencias = [
    "python-jose[cryptography]\n",
    "passlib\n",
    "bcrypt\n",
    "fastapi[standard]\n",
    "uvicorn[standard]\n",
    "sqlalchemy\n",
    "psycopg2-binary\n",
    "python-dotenv\n",
    "pydantic\n",
    "pydantic-settings\n",
    "python-multipart\n"
]

def verificar_version_python():
    """Verifica que la versión de Python sea compatible."""
    if sys.version_info < PYTHON_VERSION_MIN:
        print(f"Error: Se requiere Python {PYTHON_VERSION_MIN[0]}.{PYTHON_VERSION_MIN[1]} o superior")
        print(f"Versión actual: {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def generar_requirements():
    """Genera el archivo requirements.txt con las dependencias."""
    with open("requirements.txt", "w", encoding="utf-8") as archivo:
        archivo.writelines(dependencias)
    
    print("Archivo 'requirements.txt' generado exitosamente")
    print("\nContenido generado:")
    print(SEPARADOR)
    with open("requirements.txt", "r", encoding="utf-8") as archivo:
        print(archivo.read())

def actualizar_pip():
    """Actualiza pip a la última versión."""
    print(SEPARADOR)
    print("\nActualizando pip...\n")
    
    # Mostrar versión actual
    try:
        version_actual = subprocess.check_output(
            [sys.executable, "-m", "pip", "--version"],
            stderr=subprocess.STDOUT
        ).decode().strip()
        print(f"Versión actual: {version_actual}")
    except:
        pass
    
    print()

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ pip actualizado correctamente")
        
        # Mostrar nueva versión
        version_nueva = subprocess.check_output(
            [sys.executable, "-m", "pip", "--version"],
            stderr=subprocess.STDOUT
        ).decode().strip()
        print(f"Nueva versión: {version_nueva}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nAdvertencia: No se pudo actualizar pip: {e}")
        return False

def actualizar_pyasn1():
    """Actualiza el módulo pyasn1-modules."""
    print("\nActualizando pyasn1-modules...\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyasn1-modules"])
        print("✓ pyasn1-modules actualizado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nAdvertencia: No se pudo actualizar pyasn1-modules: {e}")
        return False

def instalar_dependencias():
    """Instala las dependencias desde requirements.txt."""
    print("\nInstalando dependencias del proyecto...\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ ¡Dependencias instaladas exitosamente!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError al instalar dependencias: {e}")
        return False
    except Exception as e:
        print(f"\nError inesperado: {e}")
        return False

def mostrar_versiones_instaladas():
    """Muestra las versiones de los paquetes principales instalados."""
    print("\n" + SEPARADOR)
    print("\nVERSIONES INSTALADAS:")
    print(SEPARADOR)
    
    # Lista de paquetes principales a verificar
    paquetes_principales = [
        "python-jose",
        "passlib",
        "bcrypt",
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
        "python-multipart"
    ]
    
    instalados = 0
    no_instalados = 0
    
    for paquete in paquetes_principales:
        try:
            resultado = subprocess.check_output(
                [sys.executable, "-m", "pip", "show", paquete],
                stderr=subprocess.STDOUT
            ).decode()
            
            # Extraer la versión del resultado
            for linea in resultado.split('\n'):
                if linea.startswith('Version:'):
                    version = linea.split(':', 1)[1].strip()
                    print(f"  {paquete:<25} {version}")
                    instalados += 1
                    break
        except subprocess.CalledProcessError:
            print(f"  {paquete:<25} No instalado")
            no_instalados += 1
    
    print(SEPARADOR)
    return instalados, no_instalados

def main():
    """Función principal que ejecuta todo el proceso."""
    tiempo_inicio = time.time()
    
    print(SEPARADOR)
    print("INSTALADOR DE DEPENDENCIAS FASTAPI")
    print(SEPARADOR)
    
    # Verificar versión de Python
    verificar_version_python()
    
    # Generar requirements.txt
    generar_requirements()
    
    # Actualizar pip
    pip_ok = actualizar_pip()
    
    # Actualizar pyasn1-modules
    pyasn1_ok = actualizar_pyasn1()
    
    # Instalar dependencias
    deps_ok = instalar_dependencias()
    
    # Mostrar versiones
    instalados, no_instalados = mostrar_versiones_instaladas()
    
    # Resumen final
    tiempo_total = time.time() - tiempo_inicio
    print("\n" + SEPARADOR)
    print("RESUMEN DE INSTALACIÓN:")
    print(SEPARADOR)
    print(f"  Pip actualizado:           {'✓' if pip_ok else '✗'}")
    print(f"  pyasn1-modules actualizado: {'✓' if pyasn1_ok else '✗'}")
    print(f"  Dependencias instaladas:    {'✓' if deps_ok else '✗'}")
    print(f"  Paquetes instalados:        {instalados}/{instalados + no_instalados}")
    print(f"  Tiempo total:               {tiempo_total:.2f} segundos")
    print(SEPARADOR)
    
    if deps_ok and no_instalados == 0:
        print("\n✓ ¡Instalación completada exitosamente!")
    else:
        print("\n⚠ Instalación completada con advertencias")

if __name__ == "__main__":
    main()
