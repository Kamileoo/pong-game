#include "Keeper.h"
#include "Game.h"
#include <iostream>
#include <sys/socket.h>
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
Keeper::Keeper()
{

}

void Keeper::createListener(int listenerPort)
{
	std::cout<<"Starting server...\n";
	int server_socket_descriptor;
    int connectionDescriptor;
    int bind_result;
    int listen_result;
    char reuse_addr_val = 1;
    struct sockaddr_in server_address;

    //inicjalizacja gniazda serwera

    memset(&server_address, 0, sizeof(struct sockaddr));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(listenerPort);
    server_socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket_descriptor < 0)
    {
        printf("Błąd przy próbie utworzenia gniazda..\n");
        exit(1);
    }
    setsockopt(server_socket_descriptor, SOL_SOCKET, SO_REUSEADDR, (char*)&reuse_addr_val, sizeof(reuse_addr_val));

    bind_result = bind(server_socket_descriptor, (struct sockaddr*)&server_address, sizeof(struct sockaddr));
    if (bind_result < 0)
    {
        printf("Błąd przy próbie dowiązania adresu IP i numeru portu do gniazda.\n");
        exit(1);
    }

    listen_result = listen(server_socket_descriptor, Keeper::QUEUE_SIZE);
    if (listen_result < 0)
    {
        printf("Error during resizing queue.\n");
        exit(1);
    }
	this->listenerFD=server_socket_descriptor;
}

void Keeper::startListen(){
	int connectionDescriptor=-1;
	std::cout<<"Waiting for connection...\n";
	while(1)
   {
       connectionDescriptor = accept(this->listenerFD, NULL, NULL);
       if (connectionDescriptor < 0)
       {
           fprintf(stderr, "Błąd przy próbie utworzenia gniazda dla połączenia.\n");
           exit(1);
       }
       this->handleConnection(connectionDescriptor);
   }

   close(this->listenerFD);

}

void Keeper::handleConnection(int connectionDescriptor)
{
    std::cout<<"New connection is handled...\n";
    bool connectionServed=false;
    //Try to add player to existing game
    for(auto &game:this->games)
    {
        if(!game->isFull())
        {
            game->addPlayer(connectionDescriptor);
            std::cout<<"Adding player to existing game...\n";
            connectionServed=true;

            if (game->isFull()) game->start();
        }
    }
    //New game needs to be created
    if(!connectionServed)
    {
        std::cout<<"Creating new game...\n";
        std::unique_ptr<Game> newGame(new Game());
        newGame->addPlayer(connectionDescriptor);
        this->games.push_back(std::move(newGame));
    }

    return;
}
