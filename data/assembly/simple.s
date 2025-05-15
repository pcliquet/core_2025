	.file	"simple.c"
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
 #APP
# 5 "data/c/simple.c" 1
	nop
	nop
	nop
	
# 0 "" 2
 #NO_APP
	li	a5,0
	li	a4,5
	sw	a4,0(a5)
	li	a4,4
	li	a3,7
	sw	a3,0(a4)
	lw	a5,0(a5)
	lw	a4,0(a4)
	add	a5,a5,a4
	sw	a5,8(zero)
	li	a5,31
	lbu	a4,0(a5)
	li	a4,1
	sb	a4,0(a5)
	lbu	a4,1(a5)
	sb	zero,1(a5)
	lbu	a4,2(a5)
	sb	zero,2(a5)
	lbu	a4,3(a5)
	sb	zero,3(a5)
 #APP
# 20 "data/c/simple.c" 1
	nop
	nop
	ecall
	
# 0 "" 2
 #NO_APP
	li	a0,0
	ret
    ecall
	.size	main, .-main
	.ident	"GCC: () 13.2.0"
