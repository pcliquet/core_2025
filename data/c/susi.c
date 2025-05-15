#define HALT 0x001F
#define MEM_BASE 0x00

int main() {
    __asm__(
        "nop\n\t"
        "nop\n\t"
        "nop\n\t");

    volatile int *mem = (int *) MEM_BASE;

    *(mem+0) = 0xffff;
    *(mem+1) = 0xaa;
    *(mem+2) = 0x05;
    *(mem+3) = 0xaa;
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
    
    return 0;
}
