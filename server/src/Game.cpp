#include "Game.h"
#include <iostream>
#include <unistd.h>
#include <functional>
#include <chrono>
#include <algorithm>
#include <iomanip>
#include <cstdint>
#include <string.h>
#include <stdlib.h>
unsigned int Game::maxNoPlayers=2;
#define WIDTH 2000
#define HIGHT 1000
#define X 0
#define Y 1
#define LEFT 0
#define RIGHT 1
#define BROAD_PERIOD 100000

Game::Game()
{
    this->isFull_=false;
}

Game::~Game()
{
}


bool Game::isFull()
{
    return this->isFull_;
}

void Game::addPlayer(int connectionDescriptor)
{
    read(connectionDescriptor,readBuff,5);
    int playerId=atoi(readBuff);
    this->playersId.push_back(playerId);
    this->playersFD.push_back(connectionDescriptor);
    if (this->playersFD.size()==Game::maxNoPlayers)this->isFull_=true;
}

int Game::updatePlayersPositions()
{
    std::cout<<"Czekanie na epoll_wait\n";
    int noFDReady=epoll_wait(epollFD,events, maxNoPlayers,-1);
    std::cout<<noFDReady<<std::endl;
    char buff[30];
    int noBytesRead=-2;
    int sign=0;
    for(int i=0; i<noFDReady; i++)
    {
        if(events[i].events & (EPOLLIN | EPOLLRDHUP | EPOLLPRI))
        {
            noBytesRead=read(playersFD[events[i].data.u32],buff,5);
            if(noBytesRead==0)return -1;
            //std::cout<<buff<<std::endl;
            sign= buff[4]=='+'? 1 : -1;
            playerMove[events[i].data.u32]+=atoi(buff)*sign;
            //std::cout<<atoi(buff)<<"LICZBA BAJTOW"<<noBytesRead<<std::endl;
        }
    }
    return 1;
}
bool Game::broadcastState()
{
    //Broad cast winner
    int idxs[2]= {-1,-1};
    bool writeOK=true;
    for(unsigned int i=0; i<this->playersFD.size(); i++)
    {
        int ballModXPos;
        if(i ==0)
        {
            idxs[0]=0;
            idxs[1]=1;
            ballModXPos=ballPosition[X];
        }
        else
        {
            idxs[0]=1;
            idxs[1]=0;
            ballModXPos=WIDTH-ballPosition[X];
        }
        if(winner!=-1)
        {
            sprintf(writeBuff, "%d,%d,%d,%d\n", -1, -1, -1, idxs[winner]);
            write(this->playersFD[i], writeBuff, strlen(writeBuff));

        }
        else
        {
            sprintf(writeBuff, "%d,%d,%d,%d\n", this->playerPositions[idxs[0]], this->playerPositions[idxs[1]],
                    ballModXPos,this->ballPosition[Y]);

            int writen_bytes=write(this->playersFD[i], writeBuff, strlen(writeBuff));
            if (writen_bytes==-1) writeOK=false;
        }

    }
    //Send players id to loser
    if(winner!=-1)
    {
            sprintf(writeBuff, "%d,%d\n", this->playersId[0],this->playersId[1]);
            write(this->playersFD[winner], writeBuff, strlen(writeBuff));
            writeOK=false;
    }
    return writeOK;
}
void Game::updateBallSpeed()
{
    //Player hits the ball
    if((ballPosition[X]<=10 && abs(playerPositions[LEFT]-ballPosition[Y])<padSize/2) ||
            (ballPosition[X]>=WIDTH-10 && abs(playerPositions[RIGHT]-ballPosition[Y])<padSize/2))
    {
        ballSpeed[X]*=-1;
        ballSpeed[Y]=2 ? rand()%2==0 : -2;
    }
    //Ball hit the wall
    if(ballPosition[Y]<=0 || ballPosition[Y]>=HIGHT)ballSpeed[Y]*=-1;

}
void Game::updateGameState()
{
    updateWinner();
    updateBallSpeed();
    for(int i=0; i<sizeof(ballSpeed)/sizeof(ballSpeed[0]); i++)
    {
        ballPosition[i]+=ballSpeed[i];
    }

    for(int i=0; i<Game::maxNoPlayers; i++)
    {
        playerPositions[i]= std::clamp(playerPositions[i]+std::clamp(playerMove[i],-100,100),0,HIGHT);
        playerMove[i]=0;
    }
}
void Game::updateWinner()
{
    if(ballPosition[X]<0) winner=1;
    if (ballPosition[X]>WIDTH) winner=0;
}

void Game::gameLoop()
{
    std::cout<<"Game loop\n";
    pthread_detach(pthread_self());
    pthread_create(&this->rcvThread, NULL, &Game::startReceivePlayersInput, (void *)this);
    std::cout<<"Receiving thread started\n";
    while(1)
    {
        std::cout<<"Bradcast"<<std::endl;
        usleep(BROAD_PERIOD);
        this->updateGameState();
        if(!this->broadcastState())break;
    }
    disconnectPlayers();

}
void Game::disconnectPlayers()
{
    for(auto &playerFD:playersFD)
    {
        close(playerFD);
    }
}

void* Game::startReceivePlayersInput(void* gamePtr)
{
    Game* game=(Game*) gamePtr;
    game->epollFD=epoll_create1(0);
    epoll_event event_struct;
    for(unsigned int i=0; i<Game::maxNoPlayers; i++)
    {
        event_struct.events=EPOLLIN;
        event_struct.data.u32=i;
        epoll_ctl(game->epollFD,EPOLL_CTL_ADD, game->playersFD[i], &(event_struct));
    }

    while(1)
    {
        if(game->updatePlayersPositions()==-1)break;
    }
    game->disconnectPlayers();
    std::cout<<"Skonczyl sie startReceiving\n";

    return NULL;
}


void* Game::startGameLoop(void* gamePtr)
{
    Game* game=(Game*)gamePtr;
    game->gameLoop();
    game->gameFinished=true;
    return NULL;
}

void Game::start()
{
    std::cout<<"Starting game...\n";

    int create_result = 0;
    create_result = pthread_create(&this->loopThread, NULL, &Game::startGameLoop, (void *)this);
    if (create_result)
    {
        printf("Error during game thread creation, error code: %d\n", create_result);
        exit(-1);
    }
}
bool Game::finished()
{
    return gameFinished;
}

