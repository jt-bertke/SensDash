#include <iostream>
#include <random>

int main() {
    // Random device for seeding
    std::random_device rd;

    // Mersenne Twister generator
    std::mt19937 gen(rd());

    // Distribution from 0 to 100
    std::uniform_int_distribution<> dist(0, 100);

    int randomNumber = dist(gen);

    std::cout << "Random number: " << randomNumber << std::endl;

    return 0;
}