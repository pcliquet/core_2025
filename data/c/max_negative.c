void main() {
    volatile int *ptr = (int *)0x00;
    for (int i = 0; i < 8; i++) {
        ptr[i] = -1 * i;
    }
    while (1);
}
//Stores negative values: 0, -1, -2, ..., -7.

//In 2's complement, negatives look like 0xFFFFFFFF, 0xFFFFFFFE, etc.