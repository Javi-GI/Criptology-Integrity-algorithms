from zlib import crc32 
import random
import pandas as pd
import time
import csv

#t = 200
#n = 6000

caracteresCadena = '0123456789'
#abcdefghijklmnopqrstuvwxyz

def cargarCSV(ficherito):
    textoCargado = []
    with open(ficherito, newline='') as csvfile:
        texto = csv.reader(csvfile, delimiter=';')

        for row in texto:
            textoCargado.append(row)
    
    return textoCargado

def h(input):
    input = bytes(input, encoding='utf-8')
    result = crc32(input)
    return result


#def r(x, index):
    caracteres = caracteresCadena
    password = (bin(x)[2:]).zfill(32)

    letra1 = caracteres[int(password[0:8], 2)%len(caracteres)]
    letra2 = caracteres[int(password[6:14], 2)%len(caracteres)]
    letra3 = caracteres[int(password[12:20], 2)%len(caracteres)]
    letra4 = caracteres[int(password[18:26], 2)%len(caracteres)]
    letra5 = caracteres[int(password[24:32], 2)%len(caracteres)]
 

    Password = letra1 + letra2 + letra3 + letra4 + letra5

    return Password

#def r(x, index):
    caracteres = caracteresCadena
    indexMod = index%(len(caracteres)-2)
    caracteres = caracteres[(indexMod+1):] + caracteres[:indexMod+1]
    password = (bin(x)[2:]).zfill(32)

    letra1 = caracteres[int(password[0:8], 2)%len(caracteres)]
    letra2 = caracteres[int(password[6:14], 2)%len(caracteres)]
    letra3 = caracteres[int(password[12:20], 2)%len(caracteres)]
    letra4 = caracteres[int(password[18:26], 2)%len(caracteres)]
    letra5 = caracteres[int(password[24:32], 2)%len(caracteres)]
 

    Password = letra1 + letra2 + letra3 + letra4 + letra5

    return Password

def r(x, index):
    Password = x%1000000
    return str(Password)


def busqueda(tabla, listaPassword, t, n):
    resultados = []
    for password in listaPassword:
        resultado = [0,0,0]
        pw = password[0]
        #print(pw)
        original = pw
        p0 = h(original) 
        p = p0
        #print(p0)

        for i in range(t):
            if p in tabla: 
                break
            p = h(r(p, i))
            #print("p: " + str(p))

        if i >= t - 1:
            print("No se encontro coincidencia.")

        else:
            pwd = tabla[p]
            print("La contraseña coincidente es: " + pwd)
            tiempo_inicio = time.time()
            tiempo_transcurrido = 0
            hPassword = h(pwd)
            i = 0
            while hPassword != p0 and i < n*t: #tiempo_transcurrido < tiempo_limite:       
                password = r(hPassword, i)
                hPassword = h(password)
                tiempo_transcurrido = time.time() - tiempo_inicio
                i = i+1

            if i < n*t: #tiempo_transcurrido < tiempo_limite:
                print("Encontrada coincidencia en hash " + str(hPassword) + " con contraseña " + password + " ----------------------------------")
                resultado = [original,pwd,password,hPassword]

            else:
                print("No se encontro en el tiempo permitido.")
                resultado = [original,pwd,0,0]
        resultados.append(resultado)
                

    return resultados

def main():
    listaResultados = []

    for i in range(100):
        t= 200
        n= 5000
        tabla = {}
        print("------ Nueva prueba ------")
        while len(tabla) < n:
            #Password al azar
            pi = ''.join(random.choice(caracteresCadena) for _ in range(6))
            p = pi

            for j in range(t - 1):
                p = r(h(p), j)

            tabla[h(p)] = pi
            #print(len(tabla))
        print("------ Tabla Creada ------")
        #print(tabla)

        passwordsList = cargarCSV("basePassword.csv")

        #print(passwordsList)

        listaResultados.append(["------- Tamaño de tabla " + str(n) +  " X " + str(t) + " --------"])
        listaResultados.append(["Original","Colision","Equivalente","Hash"])
        resultados = busqueda(tabla, passwordsList, t, n)
        listaResultados = listaResultados + resultados

        outputArcoiris = 'outputArcoirisBasePrueba.csv'
        with open(outputArcoiris, 'w', newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(listaResultados)

main()