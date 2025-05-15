	.file	"blink.c"
	.option nopic
	.attribute arch, "rv32i2p1"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-16
	sw	s0,12(sp)
	addi	s0,sp,16
.L2:
	li	a5,128
	sw	zero,0(a5)
	j	.L2
	.size	main, .-main
	.ident	"GCC: () 13.2.0"

    .global _start
    .text
_start:
    nop
    nop
    nop
    jal main

_end:
    nop
    nop
    nop
    nop
    ecall
