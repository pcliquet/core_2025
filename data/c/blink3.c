void main() {
    (*((volatile int *)128) = 1);
    volatile int i = 0;
    while (i<=150){
        if(i>=130){
            (*((volatile int *)128) = 0);
        }
        
        i++;
        (*((volatile int *)128) = 0);
    }
    (*((volatile int *)128) = 1);    
}
