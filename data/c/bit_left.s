	.file	"bit_left.c"
	.option nopic
	.attribute arch, "rv32i2p1"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.globl	main
	.type	main, @function
main:
	li	a0,32
	ret
	.size	main, .-main
	.ident	"GCC: () 13.2.0"
