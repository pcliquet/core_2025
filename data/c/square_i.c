void main() {
    __asm__(
        "nop\n\t"
        "nop\n\t"
        "nop\n\t");
        
    volatile int *ptr = (int *)0x00;
    for (int i = 0; i < 8; i++) {
        ptr[i] = i * i;
    }
    __asm__(
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "ecall\n\t"
    );
}
//Stores i² from 0 to 49: 0, 1, 4, 9, 16, 25, 36, 49.