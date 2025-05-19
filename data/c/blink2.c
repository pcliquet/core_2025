void main() {
    (*((volatile int *)128) = 1)
    volatile int i = 0;
    while (i<4999999){
        i++;
    }
    (*((volatile int *)128) = 0)
    i = 0;
    while (i<4999999){
        i++;
    }
}
