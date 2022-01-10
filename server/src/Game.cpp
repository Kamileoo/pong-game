#include "Game.h"
#include <iostream>
#include <unistd.h>
#include <functional>
unsigned int Game::noPlayers=2;


Game::Game()
{
    this->isFull_=false;
}

Game::~Game()
{
    //dtor
}


bool Game::isFull()
{
    return this->isFull_;
}

void Game::addPlayer(int connectionDescriptor)
{
    this->playersFD.push_back(connectionDescriptor);
    if (this->playersFD.size()==Game::noPlayers)this->isFull_=true;
}

void Game::gameLoop()
{
    std::cout<<"Game loop\n";
    pthread_detach(pthread_self());

    for(int i=3; i>0; i--)
    {
        char msg=static_cast<char>(i+48);
        for(auto &playerFD:this->playersFD)
        {
            write(playerFD, &msg, 1);
        }
        usleep(1000000);
    }
    for(auto &playerFD:this->playersFD)
    {
        close(playerFD);
    }
}

void* Game::startGameLoop(void* gamePtr)
{
	Game* game=(Game*)gamePtr;
	game->gameLoop();
    return NULL;
}

void Game::start()
{
    std::cout<<"Starting game...\n";

    int create_result = 0;
    create_result = pthread_create(&this->thread, NULL, &Game::startGameLoop, (void *)this);
    if (create_result)
    {
        printf("Error during game thread creation, error code: %d\n", create_result);
        exit(-1);
    }
}


