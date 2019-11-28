main: cliente.cpp servidor.cpp
	g++ PaqueteDatagrama.cpp -c
	g++ SocketDatagrama.cpp -c
	g++ Respuesta.cpp -c
	g++ Solicitud.cpp -c
	g++ cliente.cpp Solicitud.o SocketDatagrama.o PaqueteDatagrama.o -o client
	g++ servidor.cpp Respuesta.o SocketDatagrama.o PaqueteDatagrama.o -o server

