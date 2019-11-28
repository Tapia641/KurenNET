#include "Solicitud.h"
#include <iostream>
#include <cstring>
using namespace std;
unsigned int contRequest = 0;

Solicitud::Solicitud() {
	socketlocal = new SocketDatagrama(0);
}

char *Solicitud::doOperation(char *IP, int puerto, int operationId, char *arguments) {
	struct mensaje sms;
	sms.messageType = 0;
	sms.requestId = contRequest;
	printf("\nN: %u\n", contRequest);
	sms.operationId = operationId;
	memcpy(sms.arguments, arguments, sizeof(struct registro));
	PaqueteDatagrama p = PaqueteDatagrama((char *)&sms, sizeof(sms), IP, puerto);
	socketlocal->envia(p);
	PaqueteDatagrama p1 = PaqueteDatagrama(65000);
	int tam = socketlocal->recibeTimeout(p1, 2, 5000000);
	int n = 1;
	while (tam == -1 && n < 7) {
		socketlocal->envia(p);
		tam = socketlocal->recibeTimeout(p1, 2, 5000000);
		n++;
	}
	if (tam == -1) {
		cout << "Servidor no esta disponible, intente mas tarde." << endl;
		exit(0);
	}
	else
	{
		cout << "Mensaje recibido" << endl;
		struct mensaje *msj = (struct mensaje *)p1.obtieneDatos();
		contRequest++;
		return (char *)msj->arguments;
	}
}