#ifndef GAME_H
#define GAME_H
#include <vector>
#include <pthread.h>
class Game
{
    public:
    	static unsigned int noPlayers;

    	static void* startGameLoop(void*);
		//void* Game::receivePlayersInput(void* gamePtr);
        Game();
        virtual ~Game();
        bool isFull();
		void addPlayer(int connectionDescriptor);
		void start();


    private:
		bool isFull_;
		void gameLoop();
		std::vector<int> playersFD;
		pthread_t thread;
};


#endif // GAME_H
