import subprocess

# PARA USAR COMANDOS DEL SISTEMA OPERATIVO
import os, time

# TIEMPO Y COMUNICACION DE PROCESO
import shlex
from subprocess import Popen, PIPE, check_output
from threading import Timer

class Kuren:
    interfaz = ""

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
        timer = Timer(10, proc.kill)
        
        try:
            timer.start()
            stdout, stderr = proc.communicate()
            if stdout == None and stderr == None:
                print("Correct")
            else:
                print(stdout)
                print(stderr)
        finally:
            timer.cancel()
    def getNamePID(self):
        f = open ('output.txt','r+')
        lines = f.readlines()
        A =[]
        for i in range(len(lines)):
            if lines[i] == "Refreshing:\n":
                l = lines[i+1]                      
                print(l)
                x = l.split("/")
                x.reverse()
                #print(x)
                if(len(x)>3):
                     A.append(x[2])
        f.close()
        R = set(A)
        return R        
        

if __name__ == '__main__':

    
    n = Kuren()
    n.function()
    n.outputData()
    n.getNamePID()
    