void main() {
    volatile int x;
    while (1){
        *((volatile int *)128) = 1;
        *((volatile int *)128) = 0;
    }

}
