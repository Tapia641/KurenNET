# PARA USAR COMANDOS DEL SISTEMA OPERATIVO
import os, time

# Tiempo y comunicacion procesos
import shlex
from subprocess import Popen, PIPE
from threading import Timer

class Kuren:
    interfaz = ""

    def function(self):
        os.system("ip a")
        print("")
        print("---------------------------------------------------")
        print("Ingresa el nombre de la interfaz a monitorear:")
        self.interfaz = str(raw_input())
        os.system("clear")

    def outputData(self):
        print("Ejecutando NetHogs en " + self.interfaz)
        mystring = "nethogs " + self.interfaz + " >> home/tapia/Documentos/Python/data.txt"
        proc = Popen(shlex.split(mystring), stdout=PIPE, stderr=PIPE)
        timer = Timer(10, proc.kill)
        try:
            timer.start()
            stdout, stderr = proc.communicate()
            print(stdout)
            print(stderr)
        finally:
            timer.cancel()
        #out = subprocess.Popen(["nethogs", "ens33", ">>","data.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #output = subprocess.check_output("nethogs ens33", stderr=STDOUT, timeout=seconds)
        #print(output)
        #hola, err = out.communicate()
        #print(hola)
        #print(err)
        #os.system("kill -9 " + str(out.pid))

n = Kuren()
n.function()
n.outputData()
