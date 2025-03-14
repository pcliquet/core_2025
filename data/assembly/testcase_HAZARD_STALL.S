    .section    .text
    .globl      _start
    .globl      main
_start:
main:
    nop;
    addi        x9,         x0,         1       ;

    addi        x1,         x0,         3       ;
    add        x2,         x1,         x0      ;
    beq         x2,         x1,         j_eq    ;


    

j_eq:
    sw         x2,         0(x1)               ;
    addi        x3,         x0,         2       ;
    addi        x3,         x3,         1       ;
    sub         x3,         x1, x9;
    addi        x1,         x3,         1       ; 
    lw         x3,         0(x1)               ; // error
    beq        x3,         x1,         main    ;