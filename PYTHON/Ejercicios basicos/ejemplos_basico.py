


def ejercicio1():
    """
    Documentaciones utilizadas en este código:
    https://www.freecodecamp.org/espanol/news/el-operador-del-modulo-python-que-significa-el-simbolo-de-porcentaje-en-python-resuelto/
    https://es.stackoverflow.com/questions/499710/comprobar-si-existe-una-variable-en-python
    https://es.stackoverflow.com/questions/10768/crear-variables-globales-en-python
    https://stackoverflow.com/questions/73663/how-do-i-terminate-a-script
    """
    # importamos librerias necesarias
    import sys
    # Creamos variables globales para que puedan ser usadas por las funciones
    global dinero
    global moneda_25
    global moneda_5
    global moneda_1
    global end
    end = False
    # Asignamos valor a las variables creadas
    dinero = 25
    moneda_25 = 0
    moneda_5 = 0
    moneda_1 = 0

    """
    Apartado B: Añadir por terminal el numero

    Esto solo se puede usar en scripts, no aqui
    """
    dinero = int(input("Pon una cantidad de dinero: ") ) 


    # Funcion para mostrar el final
    def final():
        print('Desglose del dinero: ', dinero, '\n')
        print('\tMonedas de 25U: ', moneda_25)
        print('\tMonedas de 5U: ', moneda_5)
        print('\tMonedas de 1U: ', moneda_1)

    #Funcion para calcular el resto
    def resto(dividendo=0, divisor=0):
        if(divisor == 0):
            print("Error: Divisor no puede ser 0")
            raise SystemExit("Error: Divisor no puede ser 0")

        if (divisor != 25 and divisor != 5 and divisor != 1):
            print('Error: El divisor no puede ser disitnto de 25,5 o 1 ya que el ejericio es asi')
            raise SystemExit("Error: El divisor no puede ser disitnto de 25,5 o 1 ya que el ejericio es asi")

        mi_resto = dividendo % divisor
        cantidad = dividendo / divisor

        return int(cantidad), mi_resto


    ## Primero hacemos moneda de 25

    if end == False:

        moneda_25, el_resto_25 = resto(dividendo=dinero, divisor=25)

        if el_resto_25 == 0:
            final()
            end = True

    ## Ahora moneda de 5
    if end == False:

        moneda_5, el_resto_5 = resto(dividendo=el_resto_25, divisor=5)

        if el_resto_5 == 0:
            final()
            end = True

    if end == False:

        moneda_1, el_resto_1 = resto(dividendo=el_resto_5, divisor=1)

        final()

def ejercicio2():

    nombre = input("Como te llamas: ")
    edad = int(input("Cuantos años tienes: "))
    print("Hola", nombre + ',', "vas a cumplir", edad+1, "años")

def ejercicio3():
    nombre =  input("Como te llamas: ")
    primera_letra = nombre[0]
    primera_letra = primera_letra.upper()
    nombre_final = primera_letra + nombre[1:]
    print(nombre_final)

def ejercicio4():
    # Source - https://stackoverflow.com/q/15398427
    # Posted by user2116336, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-04-19, License - CC BY-SA 3.0
    # Documentacion: https://stackoverflow.com/questions/15398427/solving-quadratic-equation

    import math

    a = float(input("Pon el coficiente a: "))
    b = float(input("Pon el coficiente b: "))
    c = float(input("Pon el coficiente c: "))

    d = b**2-4*a*c # discriminant

    if d < 0:
        print ("This equation has no real solution")
    elif d == 0:
        x = (-b+math.sqrt(d))/ (2*a)
        print ("This equation has one solutions: ", x)
    else:
        x1 = (-b+math.sqrt(b**2-4*a*c))/ (2*a)
        x2 = (-b-math.sqrt(b**2-4*a*c))/ (2*a)
        print ("This equation has two solutions: ", x1, " and", x2)


def ejercicio5():
    from cmath import sqrt

    a = complex(input("Pon el coficiente a: "))
    b = complex(input("Pon el coficiente b: "))
    c = complex(input("Pon el coficiente c: "))

    d = complex(b**2-4*a*c)

    if d.real < 0:
        x1 =complex((-b+sqrt(b**2-4*a*c))/ (2*a))
        x2 = complex((-b-sqrt(b**2-4*a*c))/ (2*a))
        print ("This equation has two solutions: ", x1, " and", x2)
    elif d.real == 0:
        x = (-b+sqrt(d))/ (2*a)
        print ("This equation has one solutions: ", x)
    else:
        x1 = (-b+sqrt(b**2-4*a*c))/ (2*a)
        x2 = (-b-sqrt(b**2-4*a*c))/ (2*a)
        print ("This equation has two solutions: ", x1, " and", x2)
               
            
def ejercicio6():
    input('Para este truco vas a necesitar un dado...')
    input('Lanza el dado  y díjate en el resultado')
    input('Multiplícalo por 2 y suma 5 al resultado...')
    #dado = dado*2 + 5
    input('Multiplica ahora lo que tienes por 5....')
    #dado = dado*5
    input('Y ahora lanza el dado de nuevo....')
    input('y añade la puntuacion obtenida al resultado anterior....')
    # dado = dado + dado2
    resultado = int(input('Dime el resultado obtenido: '))

    print('Ahora adivinaré los resultados obtenidos....')
    input('Dejame pensar...')
    resultado = resultado - 25
    resultado_string = str(resultado)
    print('Primer numero: ', int(resultado_string[0]), ' \nSegundo número: ', int(resultado_string[1]))

import math
def raiz(a,b):
    return a ** (1/b)
if __name__ == "__main__":
    print(raiz(125,3))