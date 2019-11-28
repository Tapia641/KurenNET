#!/usr/bin/python
import subprocess

# LIBRERIAS PARA MAIL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# PARA USAR COMANDOS DEL SISTEMA OPERATIVO
import os, time

# TIEMPO Y COMUNICACION DE PROCESO
import shlex
from subprocess import Popen, PIPE, check_output
from threading import Timer

class Kuren:
    interfaz = ""
    important = 0
    limite = 0

    def dataInput(self):
        print("---------------------------------------------------")
        os.system("ifconfig")
        print("")
        print("---------------------------------------------------")
        print("Ingresa el nombre de la interfáz a monitorear:")
        self.interfaz = str(input())
        os.system("clear")
        os.system("ps aux")
        print("---------------------------------------------------")
        print("Ingresa el numero del proceso a no interferir:")
        self.important = int(input())
        os.system("clear")
        print("---------------------------------------------------")
        print("Ingresa el limite en kbs:")
        self.limite = float(input())
        os.system("clear")

    def saveOutput(self):
        #GUARDAMOS LA SALIDA CON EL FLUJO DE DATOS
        print("Ejecutando NetHogs en " + self.interfaz)
        proc = subprocess.Popen("nethogs %s -t > OUTPUT.txt" % self.interfaz, shell=True)
        timer = Timer(5, proc.kill)
        
        try:
            timer.start()
            stdout, stderr = proc.communicate()
            if stdout == None and stderr == None:
                print("Termina el comando nethogs")
            else:
                print(stdout)
                print(stderr)
        finally:
            timer.cancel()

    def getName(self):
        f = open ('OUTPUT.txt','r+')
        lines = f.readlines()
        A = dict()
        for i in range(len(lines)):
            if lines[i] == "Refreshing:\n":
                l = lines[i+1]                      
                x = l.split("/")
                x.reverse()                
                if(len(x)>3):
                    g = x[0].split("\t")
                    A.update({x[2]:[g[1],g[2].rstrip()]})                    
                    # print("THIS IS : {} {} {}".format(g[1],g[2],x[2]))                
                #      A.append(x[2])
        f.close()
        print("Esto es A:", A)
        return A       
        
    def getPID(self, myDic):
        #GUARDAMOS TODOS LOS PROCESOS ACTIVOS
        #EL COMANDO TOP HACE QUE LA TERMINAL SE TRABE
        proceso = subprocess.Popen("ps aux > PROCESS.txt", shell=True)
        timer = Timer(10, proceso.kill)
        try:
            timer.start()
            stdout, stderr = proceso.communicate()
            if stdout == None and stderr == None:
                print("Termina el comando ps aux")
            else:
                print(stdout)
                print(stderr)
        finally:
            timer.cancel()

        #DAMOS LECTURA
        f = open ('PROCESS.txt','r')
        cont = 0
        PIDS = []

        for i in f.readlines():
            if not cont == 0:
                for n in myDic:
                    values = myDic.get(n)
                    #print("Comparando value[0]: ", float(values[0]), " >= ", self.limite)
                    if n in i and float(values[0]) >= self.limite:
                        # #SE REMUEVE CARACTERES DESCONOCIDOS                        
                        string =  i.replace("[^\\dA-Za-z]", "")
                        string =  string.replace("\x1b(B\x1b[m", "")                        
                        string =  string.replace("\x1b[39;49m\x1b[K\n", "")  
                        string =  string.replace("\x1b[39;49m\x1b[K\x1b[Htop", "")                          
                        string =  string.split(" ")

                        # #AGREGAMOS SOLO ELEMENTOS NO VACIOS
                        lista =  []
                        for j in string:
                            if len(j) > 0:
                                lista.append(j)
                        
                        # #PREGUNTAMOS SI EL PID NO ESTA EN LA LISTA
                        if not lista[1] in PIDS:
                            PIDS.append(lista[1])
            cont = cont + 1
        f.close()
        
        #RETORNAMOS LOS PIDS ENCONTRADOS
        return PIDS

    def killProcess(self, LISTA):
        for i in LISTA:
            print("i: ", i)
            if not int(i) == self.important:
                os.system("kill -TERM %i" % int(i))
                print("Se mato al proceso: ", i)
                self.sendNotificacion()
    
    def sendNotificacion(self,origin,password,destinatrios_list,asunt,file_route,file_name):
        # Iniciamos los parámetros del script
        remitente = origin
        destinatarios = destinatrios_list
        asunto = asunt
        cuerpo = 'Reporte de monitoreo'
        ruta_adjunto = file_route
        nombre_adjunto = file_name

        # Creamos el objeto mensaje
        mensaje = MIMEMultipart()
        
        # Establecemos los atributos del mensaje
        mensaje['From'] = remitente
        mensaje['To'] = ", ".join(destinatarios)
        mensaje['Subject'] = asunto
        
        # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
        mensaje.attach(MIMEText(cuerpo, 'plain'))
        
        # Abrimos el archivo que vamos a adjuntar
        archivo_adjunto = open(ruta_adjunto, 'rb')
        
        # Creamos un objeto MIME base
        adjunto_MIME = MIMEBase('application', 'octet-stream')
        # Y le cargamos el archivo adjunto
        adjunto_MIME.set_payload((archivo_adjunto).read())
        # Codificamos el objeto en BASE64
        encoders.encode_base64(adjunto_MIME)
        # Agregamos una cabecera al objeto
        adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
        # Y finalmente lo agregamos al mensaje
        mensaje.attach(adjunto_MIME)
        
        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        
        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        sesion_smtp.login(origin,password)

        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)

        # Cerramos la conexión
        sesion_smtp.quit()

if __name__ == "__main__":
    n = Kuren()
    n.dataInput()
    n.saveOutput()
    A = n.getName()
    L = n.getPID(A)
    n.killProcess(L)
    
    # asunto = "REPORTE DE MONITOREO DE BW"
    # destinatarios = ['rodrigogarciaavila26@gmail.com','tapia641@gmail.com']
    # remitente = "proyectowad1221@gmail.com"
    # path = '/home/rodrigo/Escritorio/Manticora/OUTPUT.txt'
    # file_name = 'OUTPUT.txt'
    # password = 'ytrewq321'
    # n.sendNotificacion(remitente,password,destinatarios,asunto,path,file_name)