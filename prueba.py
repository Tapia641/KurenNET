import subprocess

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
        A =[]
        for i in range(len(lines)):
            if lines[i] == "Refreshing:\n":
                l = lines[i+1]                      
                x = l.split("/")
                x.reverse()
                if(len(x)>3):
                     A.append(x[2])
        f.close()
        R = set(A)
        print("Esto es R: ", R)
        return R        
        
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



if __name__ == "__main__":
    n = Kuren()
    n.dataInput()
    n.saveOutput()
    A = n.getName()
    n.getPID(A)
