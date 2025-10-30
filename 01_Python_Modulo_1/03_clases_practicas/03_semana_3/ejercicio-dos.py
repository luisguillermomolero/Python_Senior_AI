"""
while True:
    entrada = input("Ingrese la hora (0-23)")
    
    # Validación de entrada
    if entrada.isdigit():
        hora = int(entrada)
        if hora >= 0 and hora <=23:
            break
    else:
        print("Error: la hora debe estar entre 0 y 23.")

if hora >= 0 and hora < 12:
    print("Estamos en el horario de la mañana")
elif hora >= 12 and hora < 18:
    print("Estamos en el horario de la tarde")
elif hora >= 18 and hora <= 23:
    print("Estamos en el horario de noche")
"""

"""
### Calculadora de descuentos**

**Descripción:**
El usuario ingresa el valor de una compra.
Aplicar descuentos según la tabla:

| Monto         | Descuento |
| ------------- | --------- |
| ≥ 500000      | 20%       |
| 200000–499999 | 10%       |
| < 200000      | 0%        |


compra = float(input("Ingrese el valor de su compra: "))

if compra >= 500000:
    descuento = 0.20
elif compra >= 20000 and compra < 50000:
    descuento = 0.10
else:
    descuento = 0.0

valor_final = compra * (1 - descuento)

print(f"El descuento aplicado es de {descuento * 100:.0f}%")
print(f"Total a pagar: ${valor_final:,.2f}")


"""

"""
---

### Evaluador de presión arterial**

Descripción:
Ingresar la presión sistólica y diastólica, y clasificar el resultado.

| Condición                         | Mensaje |
| --------------------------------- | ------- |
| Sistólica < 90 o Diastólica < 60  | Baja    |
| Sistólica ≤ 120 y Diastólica ≤ 80 | Normal  |
| Sistólica > 120 o Diastólica > 80 | Alta    |

    


while True:
    try:
        sistolica = int(input("Por favor, Ingrese su presión sistólica:"))
        diastolica = int(input("Por favor, Ingrese su presión diastólica:"))
        
        # Validación de datos de entrada
        if sistolica <= 0 or diastolica <= 0:
            print("Los valores deben ser positivos. Intente de nuevo. \n")
            continue
        if sistolica > 300 or diastolica > 200:
            print("Los valores se encuentran fuera de un rango fisiológico\n")
            continue
        
        break
        
    except ValueError as e:
        print("Entrada no válida. Ingrese solo números enteros")
        
if sistolica < 90 or diastolica < 60:
    print("\n\n\nPELIGRO!!!! Tienes presión baja\n\n\n")
elif sistolica <= 120 and diastolica <= 80:
    print("\n\n\nPresión normal\n\n\n")
else:
    print("\n\n\nA correr al hospital....\n\n\n")

"""

"""

### Verificador de velocidad**

**Descripción:**
Pedir la velocidad de un vehículo y mostrar el estado.

| Velocidad (km/h) | Estado                 |
| ---------------- | ---------------------- |
| 0                | Detenido            |
| 1–60             | Velocidad normal    |
| 61–120           | Rápido               |
| >120             | Exceso de velocidad |


"""

while True:
    try:
        velocidad = float(input("Ingrese la velocidad del vehículo (km/h): "))
        
        if velocidad < 0:
            print("\n\nLa velocidad no puede ser negativa. Intente de nuevo. \n\n")
            continue
        if velocidad > 200:
            print("\n\nLa velocidad esta fuera de rango razonable. Intente de nuevo. \n\n")
            continue
        
        break
    
    except ValueError: 
        print("\n\nEntrada no válida. Intente de nuevo. \n\n")

if velocidad == 0:
    print("El vehiculo esta detenido")
elif velocidad > 0 and velocidad <= 60:
    print("La Velocidad es normal")
elif velocidad > 60 and velocidad <= 120:
    print("La velocidad es Rápida")
else:
    print("El vehiculo va a Exceso de velocidad")
    
"""

### Cálculo de impuesto según salario**

**Descripción:**
El usuario ingresa su salario mensual. Se aplica impuesto según rango:

| Rango               | Impuesto |
| ------------------- | -------- |
| ≤ 2.000.000         | 0%       |
| 2.000.001–5.000.000 | 10%      |
| > 5.000.000         | 20%      |

"""