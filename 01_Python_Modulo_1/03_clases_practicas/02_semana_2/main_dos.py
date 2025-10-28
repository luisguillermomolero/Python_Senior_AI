# input() = +, -, *, /, datos alfabeticos 
numero_uno = int(input("Por favor, ingrese un número:"))
numero_dos = int(input("Por favor, ingrese otro número:"))

print("Por favor, ingrese el operador de la calculadora: +, -, *, /")
opcion = input("Seleccione un operador:")

# Condicionales: if, if-elif-else
if opcion == "+":
    print(f"El resultado de la suma es = {numero_uno + numero_dos}")
if opcion == "-":
    print(f"El resultado de la resta es = {numero_uno - numero_dos}")
if opcion == "*":
    print(f"El resultado de la multiplicación es = {numero_uno * numero_dos}")
if opcion == "/":
    print(f"El resultado de la división es = {numero_uno / numero_dos}")


# Condicionales: if, if-elif-else
if opcion == "+":
    print(f"El resultado de la suma es = {numero_uno + numero_dos}")
elif opcion == "-":
    print(f"El resultado de la resta es = {numero_uno - numero_dos}")
elif opcion == "*":
    print(f"El resultado de la multiplicación es = {numero_uno * numero_dos}")
elif opcion == "/":
    print(f"El resultado de la división es = {numero_uno / numero_dos}")
else:
    print("El signo ingresado no es valido")
    

# Condicionales: if, if-elif-else
if opcion == "+":
    print(f"El resultado de la suma es = {numero_uno + numero_dos}")
else:
    if opcion == "-":
        print(f"El resultado de la resta es = {numero_uno - numero_dos}")
    else:
        if opcion == "*":
            print(f"El resultado de la multiplicación es = {numero_uno * numero_dos}")
        else:
            if opcion == "/":
                print(f"El resultado de la división es = {numero_uno / numero_dos}")

# Condicionales: if, if-elif-else
if opcion == "+":
    print(f"El resultado de la suma es = {numero_uno + numero_dos}")
else:
    if opcion == "-":
        print(f"El resultado de la resta es = {numero_uno - numero_dos}")
    else:
        if opcion == "*":
            print(f"El resultado de la multiplicación es = {numero_uno * numero_dos}")
        elif opcion == "/":
                print(f"El resultado de la división es = {numero_uno / numero_dos}")

