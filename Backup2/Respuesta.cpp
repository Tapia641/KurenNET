#include "Respuesta.h"
#include <cstring>
#include <iostream>
using namespace std;

PaqueteDatagrama p = PaqueteDatagrama(65000);

Respuesta::Respuesta(int pl) {
    socketlocal = new SocketDatagrama(pl);
    contRequest = 0;
}

struct mensaje *Respuesta::getRequest(void)
{
    int tam = socketlocal->recibeTimeout(p,2,500000);
    if (tam == -1){
        perror("Recvfrom failed");
    }
    //cout << "\nMensaje recibido" << endl;
    //cout << "Direccion: " << p.obtieneDireccion() << endl;
    //cout << "Puerto: " << p.obtienePuerto() << endl;
    struct mensaje* sms = (struct mensaje*)p.obtieneDatos();
    unsigned int reqId = 0;
    memcpy(&reqId, &sms->requestId, sizeof(sms->requestId));
    printf("\nContRequest: %u SMS->requestId: %d\n", contRequest, reqId);
        contRequest++;
        return (struct mensaje*)sms;
}

void Respuesta::sendReply(char *respuesta)
{
    struct mensaje sms;
    sms.messageType = 1;
    sms.operationId = 0;
    sms.requestId = 0;
    memcpy(sms.arguments, respuesta, sizeof(struct registro));

    p.inicializaDatos((char *)&sms);
    cout << "Mensaje enviado" << endl;
    //cout << "Direccion: " << p.obtieneDireccion() << endl;
    //cout << "Puerto: " << p.obtienePuerto() << endl;
    socketlocal->envia(p);
}