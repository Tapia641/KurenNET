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

    def getPID(self, name, upload, download):
        #GUARDAMOS TODOS LOS PROCESOS ACTIVOS
        proceso = subprocess.Popen("top > process.txt", shell=True)
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
        f = open ('process.txt','r')
        cont = 0
        pids = []
        for i in f.readlines():
            if not cont == 0:
                for n in name:
                    if n in i:                        
                        string =  i.replace("[^\\dA-Za-z]", "")
                        string =  string.replace("\x1b(B\x1b[m", "")                        
                        string =  string.replace("\x1b[39;49m\x1b[K\n", "")  
                        string =  string.replace("\x1b[39;49m\x1b[K\x1b[Htop", "")                          
                        string =  string.split(" ")
                        if string[0].isnumeric():
                            print("ESTO ES I: ",string)
                            if not int(string[0]) in pids:
                                pids.append(int(string[0]))
                        else:
                            print("ESTO ES I: ",string)
                            if not int(string[1]) in pids:
                                pids.append(int(string[1]))

            cont = cont + 1
        f.close()
        
        #IMPRIMIMOS LOS PIDS ENCONTRADOS
        print(pids)


    def function(self):
        print("---------------------------------------------------")
        os.system("ifconfig")
        print("")
        print("---------------------------------------------------")
        print("Ingresa el nombre de la interfáz a monitorear:")
        self.interfaz = str(input())
        os.system("clear")

    def outputData(self):
        #Grabamos la salida del shell
        print("Ejecutando NetHogs en " + self.interfaz)
        proc = subprocess.Popen("nethogs %s -t > output.txt" % self.interfaz, shell=True)
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
    def getNamePID(self):
        f = open ('output.txt','r+')
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
        #R = set(A)
        # print("ESTO ES R: ",A)
        return A
if __name__ == '__main__':                
    n = Kuren()
    n.function()
    n.outputData()
    A = n.getNamePID()
    #n.getPID(A, "", "")
