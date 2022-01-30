#include "Keeper.h"

#define SERVER_PORT 2000

int main(int argc, char* argv[])
{
   Keeper keeper;
   keeper.createListener(SERVER_PORT);
   keeper.startListen();

   return 0;
}
