#ifndef KEEPER_H
#define KEEPER_H
#include <vector>
#include "Game.h"
#include "memory"
using namespace std;
class Keeper
{
    public:
        Keeper();
		void startListen();
        void createListener(int listenerPort);
    private:
        vector<std::unique_ptr<Game>> games;
        static const int QUEUE_SIZE = 5;
		int listenerFD=-1;
        void handleConnection(int socket_descriptor);

};

#endif // KEEPER_H
