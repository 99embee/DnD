#include <iostream>
#include <string>

using namespace std;

class Dice {
    
private:
    int sides;
    
public:
    Dice(int sides){
        this->sides = sides;
    }

void setSides(int sides) {
    this->sides = sides;
}

int getSides() {
    return sides;
}

int roll(int times) {
    int total = 0;
    int roll = 0;
    cout << ". Rolling " << times << " times" ;
    for (int i = 1; i <= times; ++i) {
        roll = rand() % sides+1;
        cout << ". Roll " << i << ": " << roll;
        cout << ". Total: " << total ;
        total += roll;
        cout << ". Total: " << total << ".\n";
    }
return total;
}
};