// command to compile :3
// g++ Rand_num.cpp -O3 -static -o "Random Number Guesser.exe" 
#include <iostream>
#include <random>
#include <cstdlib>
#include <chrono>
#include <thread>
#include <windows.h>

// simple color settng from stackoverflow
void setColor(int color) { // Color Codes: 10 = Green, 12 = Red, 14 = Yellow, 15 = White, 11 = Cyan
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, color);
}
int random_num(){
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(1, 100);

    int rand_num = dist(gen);
    return rand_num;
}
char lower(char c){ // outsorced
    if (c >= 'A' && c <= 'Z') {
        return c + ('a' - 'A');
    }
    return c;
}
void wait(int x){
    std::this_thread::sleep_for(std::chrono::seconds(x)); // thanks stack overflow !
}

int main(){
    int random_ = random_num();
    int user_inp;
    int num_of_tries = 0;
    char skip_choice;
    choice: // acidentaly regened the num cuz i put this a bit too high
    num_of_tries++; // basicly num_of_tries = num_of_tries + 1
    setColor(11);
    std::cout   << "==============================\n" 
                << "   Random Number Guesser\n"
                << "==============================" 
                << std::endl;
    setColor(15);

    if (num_of_tries == 10) {
        setColor(12);
        std::cout << "You Seem a lil stuck, want the answer? (y/n): ";
        setColor(15);
        std::cin >> skip_choice;
        if (lower(skip_choice) == 'y'){
            setColor(10);
            std::cout << "the ans was [ " << random_ << " ]\n";
            setColor(15);
            goto end;
        } else {
            num_of_tries = 0; // reset the tries
            system("cls");
            goto choice;
        }
    }
    std::cout << "Input a number between 0 and 100: ";
    std::cin >> user_inp;

    if (user_inp == random_) { // choice = correct, ie. correct choice
        setColor(10);
        std::cout << "Correct :D\n";//  << std::endl; bad practice to spam endl as it's overhead
        setColor(15);
        goto end;
    } else if (user_inp > random_){ // choice > correct
        setColor(12);
        std::cout << "lower <--\n";
        setColor(15);
        wait(1);
        system("cls");
        goto choice;
    } else { // choice < correct
        setColor(12);
        std::cout << "higher -->\n";
        setColor(15);
        wait(1);
        system("cls"); 
        goto choice;
    }
    end:
    wait(3);

    return 0;
}