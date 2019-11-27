import subprocess

# PARA USAR COMANDOS DEL SISTEMA OPERATIVO
import os, time

# Tiempo y comunicacion procesos
import shlex
from subprocess import Popen, PIPE, check_output
from threading import Timer

class Kuren:
    interfaz = ""

    def function(self):
        os.system("ip a")
        print("")
        print("---------------------------------------------------")
        print("Ingresa el nombre de la interfaz a monitorear:")
        self.interfaz = str(input())
        os.system("clear")

    def outputData(self, file):
        #Grabamos la salida del shell
        print("Ejecutando NetHogs en " + self.interfaz)
        proc = subprocess.Popen("nethogs %s" % self.interfaz, stdout=file, shell=True)
        timer = Timer(10, proc.kill)
        
        #Visualizamos el archivo
        os.system("cat output.txt")

        try:
            timer.start()
            stdout, stderr = proc.communicate()
            print(stdout)
            print(stderr)
        finally:
            timer.cancel()
        

myfile = open("output.log", "w")
n = Kuren()
n.function()
n.outputData(myfile)