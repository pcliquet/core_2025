void main() {
    volatile int *ptr = (int *)0x00;
    for (int i = 0; i < 8; i++) {
        ptr[i] = i * 3;
    }

}

//Writes the values 0, 3, 6, 9, 12, 15, 18, 21 to memory starting at address 0x00.

//Each value is 4 bytes apart (standard int), so writes happen at 0x00, 0x04, ..., 0x1C.