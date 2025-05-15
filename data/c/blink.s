	.file	"blink.c"
	.option nopic
	.attribute arch, "rv32i2p1"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.globl	main
	.type	main, @function
    nop
    nop
    nop
main:
	addi	sp,sp,-32
	sw	s0,28(sp)
	addi	s0,sp,32
.L2:
	li	a5,128
	li	a4,1
	sw	a4,0(a5)
	li	a5,128
	sw	zero,0(a5)
	j	.L2
	.size	main, .-main
	.ident	"GCC: () 13.2.0"
