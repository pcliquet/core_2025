int main() {
    while (1) {
        // Liga LED
        (*((volatile unsigned int *)128) = 1);

        // Sleep
        for (int i = 0; i < 100; i++) asm("nop");

        // Desliga LED
        (*((volatile unsigned int *)128) = 0);
        
        // Sleep
        for (int i = 0; i < 100; i++) asm("nop");
    }

    return 0;
}