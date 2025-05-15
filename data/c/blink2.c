#include "base.h"

void main() {

    while (1) {
        sleep(500000000);
        digitalWrite(LEDR, 1);
        sleep(500000000);
        digitalWrite(LEDR, 0);
        sleep(500000000);
        digitalWrite(LEDR, 1);
        sleep(500000000);
        digitalWrite(LEDR, 0);
        sleep(500000000);
        digitalWrite(LEDR, 1);
        sleep(500000000);
        digitalWrite(LEDR, 0);
        sleep(50000000000);
        digitalWrite(LEDR, 1);
        sleep(50000000000);
        digitalWrite(LEDR, 0);
        sleep(500000000);
        digitalWrite(LEDR, 1);
        sleep(500000000);
        digitalWrite(LEDR, 0);
    }
}
