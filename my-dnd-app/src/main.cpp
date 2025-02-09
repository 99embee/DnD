#include <iostream>
#include <string>
#include "Dice.h"

using namespace std;

Dice d4(4);
Dice d6(6);
Dice d8(8);
Dice d10(10); 
Dice d20(20);
Dice d100(100);

int main() {
    srand(time(0)); // seed the random number generator
    
    cout << d6.getSides() << " sided dice, roll = " << d6.roll(1) << endl;
    cout << d20.getSides() << " sided dice, roll = " << d20.roll(1) << endl;
    cout << d4.getSides() << " sided dice, roll = " << d4.roll(1) << endl;
    return 0;
}