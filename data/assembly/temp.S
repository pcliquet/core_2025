    .section .text
    .globl      _start
    .globl      main
_start:
main:
    nop ; 
    addi x1, x0, 3 ;       # x1 = 3
    add x2, x1, x1  ;     # x2 = x1 + x1 = 6
    add x3, x2, x1   ;    # x3 = x2 + x1 = 9 (o resultado de x2 deve ser encaminhado)
    add x4, x3, x2    ;   # x4 = x3 + x2 (forwarding deve evitar stall) = 15
    add x2, x2 , x1 ;    # x2 = x2 + x1 = 9
    sw x2, 0(x4) ;        # store x2 em x4
    lw x5, 0(x4) ;        # load de x4 em x5
    add x2, x5, x1;      # x6 = x5 + x1 = 12
    sw x1 , 0(x2) ;       # store x1 em x7
    add x3 , x6 , x1;    # x3 = x6 + x1 = 3
    nop ;                 # nop para evitar que o programa termine antes do tempo    