addi x4, x0, 1
lui x9, 262144
addi x1, x0, 8
addi x2, x0, 7
addi x3, x0, 9
lui x10, 524288
sltu x20, x1, x3
sltu x20, x1, x2
sltu x20, x2, x3
sltu x20, x4, x9
sltu x20, x4, x10