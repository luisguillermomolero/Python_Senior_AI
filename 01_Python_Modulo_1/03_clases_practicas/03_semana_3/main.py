"""
    
Clasificador de temperatura:
Necesitamos desarrollar un programa que solicite al usuario una temperatura (en grados Celsius) y mostrar un mensaje dependiendo del rango:

* Menor a 0 → "Hace mucho frío"
* Entre 0 y 20 → "Clima templadito"
* Entre 21 y 30 → "Clima agradable"
* Mayor a 30 → "Terrible"

"""

temperatura = int(input("Por favor, ingrese la temperatura: "))

if temperatura < 0:
    print("Hace mucho frío")
elif temperatura <= 20:
    print("Clima templadito")
elif temperatura <= 30:
    print("Clima agradable")
else:
    print("La temperatura es Terrible...")

# Programa que permite validar si una persona es mayor de edad o no

edad = int(input("Por fvaor, ingrese su edad: "))

if edad < 18:
    print("Sumercé es menor de edad")
else:
    print("Sumercé es mayor de edad")

"""
Ejercicios:

1. Número positivo, negativo o cero

Descripción: Solicitar un número e indicar si es positivo, negativo o cero.

2. Clasificador de notas

Descripción: El usuario ingresa una nota de 0 a 100. Mostrar el nivel académico según el puntaje.

| Rango  | Mensaje   |
| ------ | ----------|
| 90–100 | Excelente |
| 70–89  | Aprobado  |
| 0–69   | Reprobado |


3. Clasificador de edad

Descripción: Pedir la edad del usuario y clasificarla en rangos.

| Rango | Mensaje      |
| ----- | ------------ |
| 0–12  | Niño         |
| 13–17 | Adolescente  |
| 18–59 | Adulto       |
| 60+   | Adulto mayor |


5. Verificar hora del día

Descripción: Pedir la hora (0 a 23) e indicar si es mañana, tarde o noche.

"""