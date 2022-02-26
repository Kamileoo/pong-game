#ifndef GAME_H
#define GAME_H
#include <vector>
#include <sys/epoll.h>

#include <pthread.h>
class Game
{
public:
    static unsigned int maxNoPlayers;

    static void* startGameLoop(void*);
    static void* startReceivePlayersInput(void* gamePtr);
    Game();
    virtual ~Game();
    bool isFull();
    void addPlayer(int connectionDescriptor);
    void start();
    bool finished();


private:
    void updateBallSpeed();
    void updateWinner();

    int updatePlayersPositions();
    bool broadcastState();
    void disconnectPlayers();
    bool isFull_;
    void gameLoop();
    int playerPositions[2]= {500,500};
    int playerMove[2]={0,0};
    int ballPosition[2]= {1000,500};
    int ballSpeed[2]={10,0};
    std::vector<int> playersFD;
    std::vector<int> playersId;

    void updateGameState();
    char writeBuff[100];
    char readBuff[100];
    int epollFD;
    epoll_event events[2];
    pthread_t loopThread;
    pthread_t rcvThread;
    bool gameFinished=false;
    int winner=-1;


    unsigned int padSize=200;
};


#endif // GAME_H
