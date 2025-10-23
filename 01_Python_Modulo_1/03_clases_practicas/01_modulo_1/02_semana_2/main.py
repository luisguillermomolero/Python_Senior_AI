# ejemplos de impresion

"""
"Luis Molero"
"Calle 10 1452 178 - 965 # 4564"
nombre = "Calle 10 1452 178 - 965 # 4564"
print("Calle 10 1452 178 - 965 # 4564")
nombre = "Luis Molero"
print("Mi nombre es: ", nombre)
print(f"Mi nombre es: {nombre}")
"""

# Operadores relacionales
variableX = 5
variableY = 10

variableZ, variableW = 8, 7

print(f" variableX == variableY: {variableX == variableY}: ") # respuesta lógica -> True o False
print(f" variableZ != variableX: {variableZ != variableX}: ")
print(f" variableY > variableW: {variableY > variableW}: ")
print(f" variableX < variableZ: {variableX < variableZ}: ")
print(f" variableW >= variableY: {variableW >= variableY}: ")
print(f" variableZ <= variableW: {variableZ <= variableW}: ")

"""
    Operadores lógicos
    
    and, or, not
    
    and = si tengo el viernes AND si tengo dinero = True
    or = si tengo el viernes or si tengo dinero = True
    
"""

tiene_dinero = True
esta_libre = False

print(f"AND: {tiene_dinero and esta_libre}")
print(f"OR: {tiene_dinero or esta_libre}") 
print(f"NOT: {not esta_libre}")


# validación manual
# Uso del condicional SI - De lo contrario -> if-else

edad = input("Ingrese un número: ")

# input() -> caracter
# int(input())
# float(input())

if edad.isdigit():
    edad = int(edad)
    print(f"La edad es valida: {edad}")
else:
    print("Error, por favor ingrese un número entero positivo")
    
tiene_dinero = True

if tiene_dinero:
    print("Salgamos este viernes")
else:
    print("Te deseo éxitos")

""" 
OPERADORES RELACIONALES

Enunciado:
Crea un programa en Python que pida al usuario ingresar dos números y muestre en pantalla el resultado de las siguientes comparaciones:

Si el primer número es mayor que el segundo.

Si el primer número es menor que el segundo.

Si ambos números son iguales.

"""

numero_uno = int(input("Ingrese un numero: "))
numero_dos = int(input("Ingrese otro numero: "))

if numero_uno > numero_dos:
    print("El número 1 es mayor al numero 2")
    print(f"{numero_uno} es mayor que {numero_dos}")
    

"""
EJERCICIOS

Ejercicio 1: Verificar mayoría de edad
1. Enunciado:
Pide la edad de una persona y muestra un mensaje si es mayor de edad (18 años o más).

2. Ejercicio 2: Determinar si un número es positivo
Enunciado:
Pide un número y muestra un mensaje si el número es positivo.

3. Ejercicio 3: Verificar rango de valores

Enunciado:
Pide un número y muestra un mensaje solo si está entre 10 y 50 (inclusive).
"""

