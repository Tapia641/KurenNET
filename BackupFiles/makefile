run: cliente.cpp Solicitud.o SocketDatagrama.o PaqueteDatagrama.o
	g++ PaqueteDatagrama.cpp -c
	g++ SocketDatagrama.cpp -c
	g++ Solicitud.cpp -c
	g++ cliente.cpp Solicitud.o SocketDatagrama.o PaqueteDatagrama.o -o client -pthread
