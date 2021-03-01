
#Importamos la libreria socket
import socket
import os
import sys

print("EMPEZAMOS")

#Creamos una lista con la direccion y el puerto donde nos conectaremos

CONEXION = (socket.gethostname(), 19001)
ARCHIVO = "operacion.txt"

usuario = "los naranjos"
contra = "morcilla1"
'''
usuario = input("Introduce el usuario: ")
contra = input("Introduce la contraseña: ")

if(usuario.__eq__("los naranjos") & contra.__eq__("morcilla1")):
    print("Acceso permitido")

else:
    print("Acceso denegado")
    cliente.close()
    sys.exit()
'''
operaciones = ["suma", "resta", "multiplicacion", "division"]

operacion = input("Introduce que operacion va a realizar ('suma', 'resta', 'multiplicacion' o 'division'): ")

while operacion not in operaciones:
    operacion = input("Introduce que operacion va a realizar ('suma', 'resta', 'multiplicacion' o 'division'): ")

while True:
    try:
        num1 = int(input("Introduce el primer numero: "))
        break
    except ValueError:
        print("Debe ser un número.")

while True:
    try:
        num2 = int(input("Introduce el segundo numero: "))
        break
    except ValueError:
        print("Debe ser un número.")

#Abrimos el archivo en modo escritura
f = open("operacion.txt", 'w')
f.write("Operacion: " + operacion + os.linesep)
f.write("op1: " + str(num1) + os.linesep)
f.write("op2: " + str(num2) + os.linesep)
f.close() #Cerramos

#Creamos el socket y nos conectamos
cliente = socket.socket()
cliente.connect(CONEXION)

#Abrimos el archivo en modo lectura binaria y leemos el contenido
with open(ARCHIVO, 'rb') as archivo:
    buffer = archivo.read()

#Mostramos el tamaño del archivo
print("El tamanio del archivo es de: ", len(buffer))

#Enviamos la cantida de bytes del archivo
print("Enviando tamanio del buffer...")
cliente.send(str(len(buffer)).encode("utf-8")) #Hay que codificarlo para poder enviarlo bien

#Esperamos la respuesta del servidor
recibido = cliente.recv(10)

if recibido.decode("utf-8") == "OK":
    print("Recibimos el OK. Enviamos el archivo")

    #Abrimos el archivo y lo leemos en modo binario
    file = open(ARCHIVO, 'rb')
    l = file.read(1024)

    #Lo leemos completamente
    while l:
        cliente.sendall(l)#Enviamos todo
        l = file.read(1024)

    file.close()#Cerramos el archivo

    print("Esperando respuesta del servidor...")

    #Creamos contador para los datos que esperamos recibir
    datosEsperados = 0

    recibido = cliente.recv(10).strip()

    print("Recibido: ", recibido.decode("utf-8"))

    if recibido.isdigit():

        datosEsperados = int(recibido.decode("utf-8"))
        cliente.send("OK".encode(("utf-8")))

        #Son los datos que debemos recibir
        datosRecibidos = 0

        #Abrimos el archivo en modo escritura binaria
        f = open("resultadoCliente.txt", 'wb')
        l = cliente.recv(datosEsperados)
        f.write(l) #Escribimos
        datosRecibidos = datosRecibidos + len(l)

        #Escribimos los datos necesarios(todos los bytes)
        while (datosRecibidos < datosEsperados):
            l = cliente.recv(1024)
            f.write(l)
            datosRecibidos = datosRecibidos + len(l)
        f.close()
        print("Fichero de respuesta recibido con éxito")

else:
    print("Recibimos", recibido.decode("utf-8"))
    print("TERMINAMOS")

cliente.close()
print("FIN")