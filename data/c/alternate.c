void main() {
    volatile int *ptr = (int *)0x00;
    for (int i = 0; i < 8; i++) {
        ptr[i] = 0xAAAAAAAA;
    }
}

//Fills memory with a repeating alternating binary pattern: 101010....