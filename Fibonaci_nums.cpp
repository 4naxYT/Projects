/*

For the people on github (students)
DO NOT ATTEMPT C++, its HARD

you need a compiler (g++ mingw)
and knoledge on syntax and working the compiler so uhh js stay away from c++


> also turbo c++ is absolute shit, dont use it
*/

#include <iostream>
#include <conio.h>
#include <cstdlib> // clear screen :D
#include <list>

std::list<int> fibonacci(int n) {
    std::list<int> nums;   // listing (finaly)

    if (n <= 0) return nums;

    // first 2 nums
    if (n >= 1) nums.push_back(0);
    if (n >= 2) nums.push_back(1);

    // loops and stuff i guess
    int a = 0, b = 1;
    for (int i = 2; i < n; ++i) {
        int next = a + b;
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
    std::list<int> result = fibonacci(x);
    std::cout << "\nFibonacci numbers: \n";

    for (int num : result) {
        std::cout << num << ",\n";
    }

    std::cout << "\n\nPress Enter To Exit...";
    _getch();  // cmd and powershell happi :3
    return 0;
}
