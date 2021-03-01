
#Importamos la libreria socket
import socket

print("EMPEZAMOS")

#Creamos la lista con los datos de la conexión
CONEXION = (socket.gethostname(), 19001)

servidor = socket.socket()

#Ponemos el servidor a escuchar
servidor.bind(CONEXION)
servidor.listen(5) #5 escuchas maximo

print("Escuchando {0} en {1}".format(*CONEXION))

while True:

    #Aceptamos las conexiones
    sck, addr = servidor.accept()
    print("Conecto a: {0} : {1} ".format(*addr))

    #Recibimos la longitud que envia el cliente
    recibido = sck.recv(1024).strip()
    print("Recibido: ", recibido.decode("utf-8"))

    #Comprobamos que se reciba
    if recibido.isdigit():
        datosEsperados = int(recibido.decode("utf-8"))
        sck.send("OK".encode("utf-8"))
        print("Envio OK", datosEsperados)

        #Contador para los bytes que recibimos
        datosRecibidos = 0

        #Abrimos el archivo en modo escritura binaria
        f = open("operacionServidor.txt", 'wb')
        l = sck.recv(datosEsperados)
        datosRecibidos = datosRecibidos + len(l)

        f.write(l) #Escribimos
        while (datosRecibidos < datosEsperados):
            l = sck.recv(1024)
            f.write(l)
            datosRecibidos = datosRecibidos + len(l)

        f.close() #Cerramos el archivo que hemos abierto para escribir en el anteriormente
        print("Fichero recibido") #Mostramos que se ha recibido

        #Abrimos el archivo de nuevo en modo lectura binaria
        f1 = open("operacionServidor.txt", 'rb')

        leerTodo = f1.readlines() #Leemos todo el archivo

        #Separamos el contenido por los dos puntos
        op = leerTodo[0].decode("utf-8").split(":")
        num_1 = leerTodo[1].decode("utf-8").split(":")
        num_2 = leerTodo[2].decode("utf-8").split(":")

        #Creamos variables para guardar la operacion, la operacion y los operandos
        resultadoOperacion = 0
        operar = op[1].strip()
        operador1 = num_1[1].strip()
        operador2 = num_2[1].strip()

        #Sumamos
        if(operar == "suma"):

            resultadoOperacion = int(operador1) + int(operador2)

        #Restamos
        if (operar == "resta"):
            resultadoOperacion = int(operador1) - int(operador2)

        #Dividimos
        if (operar == "division"):
            resultadoOperacion = int(operador1) / int(operador2)

        #Multiplicamos
        if (operar == "multiplicacion"):
            resultadoOperacion = int(operador1) * int(operador2)

        #Abrimos un nuevo archivo donde guardaremos la respuesta del servidor con el resultado
        f = open("respuestaServidor.txt", "w")
        f.write("Resultado: " + str(resultadoOperacion))

        print("Operacion: ", operar)
        print("Numero 1: ", operador1)
        print("Numero 2: ", operador2)
        print("El resultado: ", resultadoOperacion)
        f.close()

        #Abrimos el archivo en modo lectura binaria
        with open("respuestaServidor.txt", "rb") as archivo:
            buffer = archivo.read()

        #Mostramos el tamanio del archivo
        print("Tamanio del archivo: ", len(buffer))
        sck.send(str(len(buffer)).encode("utf-8"))
        recibido = sck.recv(10)

        #Si recibimos el OK, enviamos el fichero con la respuesta
        if(recibido.decode("utf-8") == "OK"):

            print("Enviando fichero con la respuesta...")

            #Abrimos el archivo en modo lectura binario
            file2 = open("respuestaServidor.txt", "rb")
            l = file2.read(1024)

            #Leemos y enviamos el archivo
            while l:
                sck.sendall(l)  # Enviamos todo
                l = file2.read(1024)

            file2.close()  # Cerramos el archivo

            print("El fichero se ha enviado correctamente")

    else:
        sck.send("ERROR".encode("utf-8"))
    print("Servicio termina")

sck.close()

print("FIN")