
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
    print("Conexto a: {0} : {1} ".format(*addr))

    #Recibimos la longitud que envia el cliente
    recibido = sck.recv(1024).strip()
    print("Recibido: " , recibido.decode("utf-8"))

    #Comprobamos que se reciba
    if recibido.isdigit():
        datosEsperados = int(recibido.decode("utf-8"))
        sck.send("OK".encode("utf-8"))
        print("Envio OK", datosEsperados)

        #Contador para los bytes que recibimos
        datosRecibidos = 0

        #Abrimos el archivo en modo escritura binaria
        f = open("resultado.txt",'wb')
        l = sck.recv(datosEsperados)
        datosRecibidos = datosRecibidos + len(l)

        f.write(l) #Escribimos
        while (datosRecibidos < datosEsperados):
            l = sck.recv(1024)
            f.write(l)
            datosRecibidos = datosRecibidos + len(l)

        f.close() #Cerramos el archivo que hemos abierto para escribir en el anteriormente
        print("Fichero recibido") #Mostramos que se ha recibido

    else:
        sck.send("ERROR".encode("utf-8"))
    print("Servicio termina")

sck.close()

print("FIN")