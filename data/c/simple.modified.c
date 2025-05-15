
        __asm__(
            "nop\n\t"
            "nop\n\t"
            "nop\n\t");
        #define HALT 0x001F
#define MEM_BASE 0x00

int main() {

    volatile int *mem = (int *) MEM_BASE;

    *(mem + 0) = 5;   // endereço 0
    *(mem + 1) = 7;   // endereço 1

    int a = *(mem + 0);  // lê mem[0]
    int b = *(mem + 1);  // lê mem[1]

    *(mem + 2) = a + b;  // escreve em mem[2]

    *(volatile int*)HALT = 1; // 🛑 sinaliza parada


    return 0;
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
        