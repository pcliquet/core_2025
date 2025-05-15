	.file	"corsi.c"
	.option nopic
	.attribute arch, "rv32i2p1"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.globl	main
	.type	main, @function
main:
 #APP
# 5 "data/c/corsi.c" 1
	nop
	nop
	nop
	
# 0 "" 2
 #NO_APP
	li	a5,65536
	addi	a5,a5,-1
	sw	a5,0(zero)
	li	a5,170
	sw	a5,4(zero)
	li	a4,5
	sw	a4,8(zero)
	sw	a5,12(zero)
 #APP
# 16 "data/c/corsi.c" 1
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	ecall
	
# 0 "" 2
 #NO_APP
	li	a0,0
	ret
	.size	main, .-main
	.ident	"GCC: () 13.2.0"
