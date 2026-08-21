/*

g++ "Fibonaci Nums.cpp" -O3 -static -o Fibonaci.exe  

For the people on github (students)
DO NOT ATTEMPT C++, its HARD
you need a compiler (g++ mingw)
and knoledge on syntax and working the compiler so uhh js stay away from c++

> also turbo c++ is absolute shit, dont use it

Project docs:
int -> too small
float ->too small
double ...

--unsigned long long is best for this i think--
edit2: unsigned __int128 is better

could use boost multi-precision but it's overkill for ts

*/
#include <iostream>
#include <conio.h>
#include <cstdlib> // clear screen :D
#include <vector>
#include <string> // str manipulation addons
#include <algorithm>  // for reverse()

// Helper for printing this weird number
void print_u128(unsigned __int128 num) { // thanks to stack overflow
    if (num == 0) {
        std::cout << '0';
        return;
    }
    std::string str;
    while (num > 0) {
        int digit = num % 10;                // extract last digit
        str.push_back('0' + digit);          // convert to char
        num /= 10;
    }
    std::reverse(str.begin(), str.end());   // we built it backwards
    std::cout << str;
}

std::vector<unsigned __int128> fibonacci(int amt) { // int and float's too small
    std::vector<unsigned __int128> nums;

    if (amt <= 0) return nums;
    nums.reserve(amt);          // pre‑allocate for speed

    nums.push_back(0);
    if (amt == 1) return nums;
    nums.push_back(1);

    unsigned __int128 a = 0, b = 1;
    const unsigned __int128 MAX = ~((unsigned __int128)0); // max val i assume

    for (int i = 2; i < amt; ++i) { // complicated math stuffs

        if (b > MAX - a) { // compares max allowed bits in our `var` to what we need to it to be
            std::cerr << "Warning: overflow at term " << i << ", stopping.\n"; // prints an error msg or smth
            break; // stops calc loop
        }

        unsigned __int128 next = a + b;
        nums.push_back(next);
        a = b;
        b = next;
    }

    return nums;
}

int main() {
    int x;

    system("cls"); // cmd users

    std::cout << "Enter amount of Fibonacci numbers: ";
    std::cin >> x;

    auto result = fibonacci(x);

    std::cout << "\nFibonacci numbers: \n";

    for (size_t i = 0; i < result.size(); ++i) { // thanks to stack overflow
        print_u128(result[i]);
        if (i + 1 < result.size()) std::cout << ",\n";
    }

    std::cout << "\n\nPress Enter To Exit...";
    _getch();  // cmd and powershell happi :3
    return 0;
}