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
        print("Ingresa el nombre de la interfaz a monitorear:")
        self.interfaz = str(input())
        os.system("clear")

    def outputData(self):
        #Grabamos la salida del shell
        print("Ejecutando NetHogs en " + self.interfaz)
        proc = subprocess.Popen("nethogs %s -b > output.txt" % self.interfaz, shell=True)
        timer = Timer(10, proc.kill)
        
        try:
            timer.start()
            stdout, stderr = proc.communicate()
            if stdout == "None" and stderr == "None":
                print("Correct")
            else:
                print(stdout)
                print(stderr)
        finally:
            timer.cancel()
        
n = Kuren()
n.function()
n.outputData()