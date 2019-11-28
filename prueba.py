#!/usr/bin/python
import subprocess

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
    
    def sendNotificacion(self):
        pass

if __name__ == "__main__":
    n = Kuren()
    n.dataInput()
    n.saveOutput()
    A = n.getName()
    L = n.getPID(A)
    n.killProcess(L)