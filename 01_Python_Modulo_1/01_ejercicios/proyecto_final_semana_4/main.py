from typing import Dict, List, Optional

# Lista global de estudiantes
estudiantes: List[Dict[str, any]] = []


def validar_edad(mensaje: str) -> Optional[int]:

    while True:
        try:
            edad = int(input(mensaje))
            if edad > 0 and edad <= 120:  # Validación de rango realista
                return edad
            else:
                print("⚠️ Error: la edad debe estar entre 1 y 120 años.")
        except ValueError:
            print("⚠️ Error: debe ingresar un número entero válido.")


def validar_nota(mensaje: str) -> Optional[float]:

    while True:
        try:
            nota = float(input(mensaje))
            if 0 <= nota <= 5:
                return nota
            else:
                print("⚠️ Error: la nota debe estar entre 0 y 5.")
        except ValueError:
            print("⚠️ Error: debe ingresar un número válido.")


def validar_nombre(mensaje: str) -> Optional[str]:

    while True:
        nombre = input(mensaje).strip()
        if nombre and nombre.replace(' ', '').isalpha():
            return nombre
        elif not nombre:
            print("⚠️ Error: el nombre no puede estar vacío.")
        else:
            print("⚠️ Error: el nombre solo debe contener letras.")


def registrar_estudiante() -> None:

    print("\n=== REGISTRO DE ESTUDIANTE ===")
    
    nombre = validar_nombre("Ingrese el nombre del estudiante: ")
    if nombre is None:
        return
    
    edad = validar_edad("Ingrese la edad: ")
    if edad is None:
        return
    
    nota = validar_nota("Ingrese la nota final (0-5): ")
    if nota is None:
        return

    estudiante: Dict[str, any] = {
        "nombre": nombre.title(),  # Capitaliza correctamente
        "edad": edad,
        "nota": nota
    }
    estudiantes.append(estudiante)
    print("✅ Estudiante registrado correctamente.")


def mostrar_estudiantes() -> None:

    print("\n=== LISTADO DE ESTUDIANTES ===")
    
    if not estudiantes:
        print("📭 No hay estudiantes registrados.")
    else:
        print(f"\nTotal de estudiantes: {len(estudiantes)}\n")
        for i, e in enumerate(estudiantes, 1):
            print(f"{i}. Nombre: {e['nombre']:15} | Edad: {e['edad']:3} años | Nota: {e['nota']:.2f}")


def buscar_estudiante() -> None:

    print("\n=== BÚSQUEDA DE ESTUDIANTE ===")
    
    if not estudiantes:
        print("📭 No hay estudiantes registrados.")
        return
    
    nombre = input("Ingrese el nombre a buscar: ").strip().lower()
    
    if not nombre:
        print("⚠️ Error: debe ingresar un nombre para buscar.")
        return
    
    encontrados = [e for e in estudiantes if nombre in e["nombre"].lower()]
    
    if encontrados:
        print(f"\n✅ Se encontraron {len(encontrados)} estudiante(s):\n")
        for i, e in enumerate(encontrados, 1):
            print(f"{i}. Nombre: {e['nombre']:15} | Edad: {e['edad']:3} años | Nota: {e['nota']:.2f}")
    else:
        print(f"❌ No se encontraron estudiantes con el nombre '{nombre}'.")


def calcular_promedio() -> None:

    print("\n=== ESTADÍSTICAS GENERALES ===")
    
    if not estudiantes:
        print("📭 No hay estudiantes registrados.")
        return
    
    notas = [e["nota"] for e in estudiantes]
    promedio = sum(notas) / len(notas)
    nota_max = max(notas)
    nota_min = min(notas)
    
    print(f"\n📊 Estadísticas:")
    print(f"   Promedio general: {promedio:.2f}")
    print(f"   Nota máxima: {nota_max:.2f}")
    print(f"   Nota mínima: {nota_min:.2f}")
    print(f"   Total de estudiantes: {len(estudiantes)}")


def menu() -> None:

    while True:
        print("\n" + "="*50)
        print("    SISTEMA DE REGISTRO DE ESTUDIANTES")
        print("="*50)
        print("1. Registrar estudiante")
        print("2. Mostrar estudiantes")
        print("3. Buscar estudiante")
        print("4. Calcular promedio general")
        print("5. Salir")
        print("="*50)
        
        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            registrar_estudiante()
        elif opcion == "2":
            mostrar_estudiantes()
        elif opcion == "3":
            buscar_estudiante()
        elif opcion == "4":
            calcular_promedio()
        elif opcion == "5":
            print("\n👋 Gracias por usar el sistema. ¡Hasta pronto!")
            break
        else:
            print("⚠️ Opción inválida, intente de nuevo.")


def main() -> None:
    menu()


if __name__ == "__main__":
    main()
