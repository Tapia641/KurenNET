//Programa para crear registros de votos [celular, CURP, partido, separador], con el campo "celular" como clave 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include "Solicitud.h"
#include <sys/time.h>
#include <unistd.h>
#include <iostream> 
#include <list> 
#include <thread>  
#include <iterator> 

using namespace std;

/*---------------------------------------------*/
int n = 0;
list <int> lista1, lista2, lista3;
list<int>::iterator itr1, itr2, itr3;

struct registro GenerarVoto(int j, int tipo){
	char telefono[11], curp[19], t[11], sexo;
	int i, destino, opcion, elemento;
	struct registro reg1;
	//Partidos disponibles 2018
	char const partidos[9][4] = {"PRI", "PAN", "PRD", "P_T", "VDE", "MVC", "MOR", "PES", "PNL"};
	//Entidades federativas
	char const entidad[32][3] =  {"AS", "BC", "BS", "CC", "CS", "CH", "CL", "CM", "DF", "DG", "GT", "GR", "HG", "JC", "MC", "MN", "MS", "NT", "NL", "OC", "PL", "QT", "QR", "SP", "SL", "SR", "TC", "TL", "TS", "VZ", "YN", "ZS"};
	//Obtiene un elemento aleatorio de la lista de telefonos y lo elimina de la lista para evitar la repeticion
	i = n - j;
	elemento = rand()%i;	

	if (tipo == 1 )
	{
		itr1 = lista1.begin();
	}else if (tipo == 2)
	{
		itr2 = lista2.begin();
	}else{
		itr3 = lista3.begin();
	}
	
	
	for(int k = 0; k < elemento; k++){
		if (tipo == 1)
		{
			++itr1;
		}else if (tipo == 2)
		{
			++itr2;
		}else{
			++itr3;
		}
	}
	
		if (tipo == 1)
		{
			elemento = *itr1;
		}else if (tipo == 2)
		{
			elemento = *itr2;
		}else{
			elemento = *itr3;
		}

		
	if (tipo == 1 )
	{
		lista1.erase(itr1);
	}else if (tipo == 2)
	{
		lista2.erase(itr2);
	}else{
		lista3.erase(itr3);
	}
	
	sprintf(telefono, "5%9d", elemento);
	strcpy(reg1.celular, telefono);

	if(rand()%2 == 0)
		sexo = 77;
	else
		sexo = 72;
	i = rand()%32;
	sprintf(curp, "%c%c%c%c%c%c%c%c%c%c%c%s%c%c%c%c%c", 65 + rand()%25 , 65 + rand()%25, 65 + rand()%25, 65 + rand()%25, rand()%10 + 48, rand()%10 + 48, rand()%10 + 48, rand()%10 + 48, rand()%10 + 48, rand()%10 + 48, 
	sexo, entidad[i], 65 + rand()%25, 65 + rand()%25, 65 + rand()%25, rand()%10 + 48, rand()%10 + 48);
	strcpy(reg1.CURP, curp);
	i = rand()%9;
	strcpy(reg1.partido, partidos[i]);
	return reg1;
}
/*---------------------------------------------*/

void enviar1(char * ip,int puerto){
	// Procesa de 0 - 3
	Solicitud s;
	timeval res;
	int cont = 0;
	while(cont < n) {
		int port;
		struct registro r = GenerarVoto(cont, 1);
		string lastc = string(r.celular);
		lastc=lastc.back();
		int lastN = atoi(lastc.c_str());
		if (lastN >= 0 && lastN <= 3)
		{
			cout << "Hilo 1: " << endl;
			memcpy(&res, s.doOperation(ip, puerto, 1, (char *)&r),sizeof(timeval));
			cout << res.tv_sec << endl;
			cout << res.tv_usec << endl;
		}
		cont++;
	}
	cout<< "Hilo 1, Procese: " << cont<<endl;
}

void enviar2(char * ip,int puerto){
	// Procesa de 4 - 6
	Solicitud s;
	timeval res;
	int cont = 0;
	while(cont < n) {
		int port;
		struct registro r = GenerarVoto(cont, 2);
		string lastc = string(r.celular);
		lastc=lastc.back();
		int lastN = atoi(lastc.c_str());
		if (lastN >= 4 && lastN <= 6)
		{
			cout << "Hilo 2: " << endl;
			memcpy(&res, s.doOperation(ip, puerto, 1, (char *)&r),sizeof(timeval));
			cout << res.tv_sec << endl;
			cout << res.tv_usec << endl;
		}
		cont++;
	}
	cout<< "Hilo 2, Procese: " << cont<<endl;
}

void enviar3(char * ip,int puerto){
	// Procesa de 7 - 9
	Solicitud s;
	timeval res;
	int cont = 0;
	while(cont < n) {
		int port;
		struct registro r = GenerarVoto(cont, 3);
		string lastc = string(r.celular);
		lastc=lastc.back();
		int lastN = atoi(lastc.c_str());
		if (lastN >= 7 && lastN <= 9)
		{
			cout << "Hilo 3: " << endl;
			memcpy(&res, s.doOperation(ip, puerto, 1, (char *)&r),sizeof(timeval));
			cout << res.tv_sec << endl;
			cout << res.tv_usec << endl;
		}
		cont++;
	}
	cout<< "Hilo 3, Procese: " << cont<<endl;
}

struct Servidor{
	char * ip;
	int port;
};

int main(int argc, char *argv[]){
	
	if (argc != 8)
	{
		//7 IP PORT IP PORT IP PORT
		printf("Forma de uso: %s ip_servidor n\n", argv[0]);
		exit(0);
	}
	Servidor s1;
	Servidor s2;
	Servidor s3;
	s1.ip=argv[1];
	s1.port=atoi(argv[2]);
	s2.ip=argv[3];
	s2.port=atoi(argv[4]);
	s3.ip=argv[5];
	s3.port=atoi(argv[6]);
	n = atoi(argv[7]);
	int cont = 0;

	//Llena una lista con numeros telefonicos de 9 digitos secuenciales creibles
		srand(time(NULL));
		int inicial = 500000000 + rand()%100000000;
		for (int i = inicial; i < inicial + n; i++) 
		{ 
			lista1.push_back(i);
			lista2.push_back(i);
			lista3.push_back(i);
		}
		
		thread t1(enviar1,s1.ip,s1.port);
		thread t2(enviar2,s2.ip,s2.port);
		thread t3(enviar3,s3.ip,s3.port);

		t1.join();
		t2.join();
		t3.join();

	return 0;
}
