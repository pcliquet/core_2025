	.file	"multply.c"
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
	sw	zero,0(zero)
	li	a5,3
	sw	a5,4(zero)
	li	a5,6
	sw	a5,8(zero)
	li	a5,12
	li	a4,9
	sw	a4,0(a5)
	sw	a5,16(zero)
	li	a5,15
	sw	a5,20(zero)
	li	a5,18
	sw	a5,24(zero)
	li	a5,21
	sw	a5,28(zero)
	ret
    ecall
	.size	main, .-main
	.ident	"GCC: () 13.2.0"
