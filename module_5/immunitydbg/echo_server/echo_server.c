/*
 * INCLUDING THE PROPER LIBRARIES
 * DEPENDING ON OPERATING SYSTEM
 *
 * */

#if defined(unix) || defined(__unix__) || defined(__unix)
	#define PREDEF_PLATFORM_UNIX 1				// okay we are in a unix machine
	#include <sys/socket.h>					// including unix socket headers
	#include <netdb.h>					// needed for unix socket
	#include <netinet/in.h>					// for internet protocol family
	#include <unistd.h>					// needed for unix read/write
#elif defined(__WIN32)
	#define PREDEF_PLATFORM_MS 1				// now we are in a windows machine
	#include <winsock2.h>					// including ms socket headers
	#include <io.h>						// needed for ms read/write
	#pragma comment(lib, "ws2_32.lib")			// telling linker to link winsock library
#endif

#include <stdio.h>						// crossed platform headers
#include <string.h>						// string header, for strcpy
#include <stdlib.h>						// stardard lib, for exit()


int main(int argc, char** argv)
{
	// operating system platform check
	#if PREDEF_PLATFORM_UNIX == 1
		printf("\n[!] We are in an unix host\n");
	#elif PREDEF_PLATFORM_MS == 1
		printf("\n[!] We are in a ms host\n");
	#else
		printf("\n[!] Unable to identify the host machine");
		printf("[!] Exiting...\n");
		exit(EXIT_FAILURE);
		return 1;
	#endif

	// initalizing variables
	int MAX_CONN = 1;					// max connection allowed for this tcp socket server
	int yes = 1;						// used to reuse address in socket option
	char send_str[100];					// string to send
	char recv_str[100];					// string recieved
	int listen_fd, communicate_fd;				// file descriptors used for sockets

	struct sockaddr_in serv_addr;				// struct to store socket server address info

	#if PREDEF_PLATFORM_MS == 1				// if we are in a microsoft windows host system
		WSADATA wsa;					// its address needed for initalizing windows socket api (WSA)
        	struct sockaddr_in client;      		// used for the address inside accept function
        	int c;                          		//used to store the size of sockaddr_in struct

	        memset((WSADATA*) &wsa, 0, sizeof(wsa));
		if (WSAStartup(MAKEWORD(2,2), &wsa) != 0)	// initialzing wsa using wsastartup
		{
			printf("\n[!] Error: %d\n", WSAGetLastError());
			printf("\n[!] Failed to initialize winsock api, shutting down...\n");
			return 1;				// exiting
		}else
		{
			printf("\n[!] Windows Socket API Initialized!\n");
		}
	#endif
	
	listen_fd = socket(AF_INET, SOCK_STREAM, 0);		// socket method from socket.h returns a file descriptor
								// takes params, af_inet = ip fam, sock_stream = tcp type socket
								// 0 for deafult protocol for the requets socket type
	if (listen_fd == -1){
		printf("\n[!] We couldn't establish a socket descriptor for listening");
		printf("\n[!] Exiting...");
		exit(EXIT_FAILURE);
		return 1;
	}
	printf("\n[!] We have established a server socket\n");

	//setting the socket options at socket level, not protocol lvl, with resuseable address
	// with also the address of the interger 1 for yes, lets re use addressees, and the size of that 1
	// which is different across different platforms
	printf("\n[!] Setting the resuable address to true\n");
	if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, (const void*) &yes, sizeof(int)) == -1){
		printf("\n[!] We couldn't set the socket option for reusable address");
		printf("\n[!] Exiting...");
		exit(EXIT_FAILURE);
		return 1;
	}


	memset(&serv_addr, 0, sizeof(serv_addr));		// clearing memory for declared server addy info structure
								// takes in the address of declared struct, and the size to clear
								// it will place zero value bytes in the area pointed by the address
	serv_addr.sin_family = AF_INET;				// setting/populating up all the server address info
	serv_addr.sin_addr.s_addr = htons(INADDR_ANY);		// this script will allow any ip to connect
								// htons used to make sure right formatting before going into the struct
	serv_addr.sin_port = htons(22000);			// using port 22000, htons to ensure formatting

	// binding using the bind method provided by socket.h: binding the socket returned file descriptor
	// with a struct pointer pointing to the address of server address struct declared earlier
	// and also need to feed the function the size of the server address struct
	bind(listen_fd, (struct sockaddr*) &serv_addr, sizeof(serv_addr));		//binding address to socket

	listen(listen_fd, MAX_CONN);							// after binding we listen for 5 connections

	printf("\n[!] We have sucessfully binded localhost IP, and listening on port 22000\n");


	// accept is a blocking call, blocking execution until a connection is made,
	// once made the accept method will return a new file descriptor for communication
	// purpose with the client socket, and waits for another connection, until the max no. of connection
	// takes in the socket file descriptor we are currently listening to,
	// a pointer to a socketaddr struct of the particular client socket, which is NULL for any,
	// third parameter NULL for size of struct
	
	#if PREDEF_PLATFORM_UNIX == 1
        	communicate_fd = accept(listen_fd, (struct sockaddr*) NULL, NULL);
	#elif PREDEF_PLATFORM_MS == 1
        	c = sizeof(struct sockaddr_in);
        	communicate_fd = accept(listen_fd, (struct sockaddr*) &client, &c);	
	#endif 

	if (communicate_fd == -1)
    	{
        printf("\n[!] Unable to establish connection with client, and get communicatefd...\n");
        printf("\n[!] Shutting down\n");
        return 1;
    	}

	printf("\n[!] We have found a connection, getting ready to EcHoOoo\n");

	while(1)
	{
		memset(recv_str, 0, sizeof(recv_str));			// clearing out echo_str that was declared earlier, notice passing in
									// its name is = to its address, because its a char array, and all arrays
									// are pointer themselves
		memset(send_str, 0, sizeof(send_str));

		#if PREDEF_PLATFORM_UNIX == 1
	        	read(communicate_fd, recv_str, 100);		// reading from a file descriptor, storing it in a string(char array)
		#elif PREDEF_PLATFORM_MS == 1
            		recv(communicate_fd, recv_str, 100, 0);		// reading from a file descriptor, storing it in a string(char array), 
									// using recv for ms apps, last param is for flag opt purposes,
                                                        		// we put 0, because  ms doc sucks
		#endif

		if (strlen(recv_str) == 0)				// to check if client terminates, the recived string, 
									// or sent from client is emtpy, 
		{							// because the client disconnects and sent a termination of program
			printf("\n[!] Client disconnected, getting ready to shut down...\n");
			break;						// and recieved string will eventually get a one that is no length string
		}							// while all other time its just waiting for client sender, 
									// now breaking out loop

		printf("\n[!] Echoing back: %s\n", recv_str);		// printing info on our screen

		// this is where we have a BoF problem
		strcpy(send_str, recv_str);				// using strcpy to copy the recieved string to the send string var
									// w/o limit test, memory buffer could over flow


		// writing to the communicate file descriptor, writing it the send string
		// also inputting the size fo the send string's length plus 1, for the null terminator?
		#if PREDEF_PLATFORM_UNIX == 1
            		write(communicate_fd, send_str, strlen(send_str)+1);
        	#elif PREDEF_PLATFORM_MS == 1
            		send(communicate_fd, send_str, strlen(send_str)+1, 0);      	//using send for ms apps, and 
											//the last params is for flag opt purposes, 
											//we put 0, bc ms doc sucks
        #endif

	}

	#if PREDEF_PLATFORM_MS == 1
		printf("\n[!] Getting ready to shut down winsock api, and ms system\n");
		printf("\n[!] Closing socket, shutting off...\n");
		closesocket(communicate_fd);
		closesocket(listen_fd);
		WSACleanup();
	#elif PREDEF_PLATFORM_UNIX == 1
		printf("\n[!] Getting ready to shutdown unix system\n");
		printf("\n[!] Closing socket, shutting off...\n");
		close(communicate_fd);
		close(listen_fd);

	#endif

	return 0;






}

