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

    def dataInput(self):
        print("---------------------------------------------------")
        os.system("ifconfig")
        print("")
        print("---------------------------------------------------")
        print("Ingresa el nombre de la interfáz a monitorear:")
        self.interfaz = str(input())
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
        A =dict()
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
        return A       
        
    def getPID(self, name):
        #GUARDAMOS TODOS LOS PROCESOS ACTIVOS
        #EL COMANDO TOP HACE QUE LA TERMINAL SE TRABE
        proceso = subprocess.Popen("top > PROCESS.txt", shell=True)
        timer = Timer(10, proceso.kill)
        try:
            timer.start()
            stdout, stderr = proceso.communicate()
            if stdout == None and stderr == None:
                print("Termina el comando top")
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
                for n in name:
                    if n in i:
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
                        if not lista[0] in PIDS:
                            PIDS.append(lista[0])
            cont = cont + 1
        f.close()
        
        #IMPRIMIMOS LOS PIDS ENCONTRADOS
        print(PIDS)
    
    def sendMail(self,origin,password,destinatrios_list,asunt,file_route,file_name):
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
