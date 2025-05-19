	.file	"blink3.c"
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
	addi	sp,sp,-16
	li	a5,1
	sw	a5,128(zero)
	sw	zero,12(sp)
	j	.L2
.L3:
	lw	a5,12(sp)
	addi	a5,a5,1
	sw	a5,12(sp)
	sw	zero,128(zero)
.L2:
	lw	a4,12(sp)
	li	a5,150
	bgt	a4,a5,.L6
	lw	a4,12(sp)
	li	a5,129
	ble	a4,a5,.L3
	sw	zero,128(zero)
	j	.L3
.L6:
	li	a5,1
	sw	a5,128(zero)
	addi	sp,sp,16
	jr	ra
	.size	main, .-main
	.ident	"GCC: () 13.2.0"
