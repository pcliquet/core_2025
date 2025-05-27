import pytest
from cocotb.binary import BinaryValue

import lib
from test_CPU_package import CPU
from test_CPU_STAGE_IF import CPU_STAGE_IF
from test_CPU_STAGE_ID import CPU_STAGE_ID
from test_CPU_STAGE_EX import CPU_STAGE_EX
from test_CPU_STAGE_MEM import CPU_STAGE_MEM
from test_CPU_STAGE_WB import CPU_STAGE_WB
from test_CPU_BRANCH_FORWARDING_UNIT import CPU_BRANCH_FORWARDING_UNIT
from test_CPU_EXECUTION_FORWARDING_UNIT import CPU_EXECUTION_FORWARDING_UNIT
from test_CPU_HAZZARD_CONTROL_UNIT import CPU_HAZZARD_CONTROL_UNIT

def read_expected_memory_dict(path):
    memory = {}
    with open(path, 'r') as f:
        for line in f:
            if ':' in line:
                addr, val = line.strip().split(':')
                binv = val.strip().replace('"', '').replace(',', '')
                memory[int(addr)] = binv.zfill(32)
    return memory

def test_in_out_rom(input_mem, output_mem):
    GREEN, RED, YELLOW, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[0m"

    for addr in input_mem:
        if addr not in output_mem:
            print(f"{YELLOW}address {addr} missing in output{RESET}")
            continue
        inp = input_mem[addr].zfill(32)
        out = output_mem[addr]
        if inp == out:
            print(f"{GREEN}match at {addr}: {inp}{RESET}")
        else:
            print(f"{RED}mismatch at {addr}{RESET}")
            print(f"{RED}  input : {inp}{RESET}")
            print(f"{RED}  output: {out}{RESET}")

class CPU_TOP_LEVEL(lib.Entity):
    _package = CPU

    clock = lib.Entity.Input_pin
    clear = lib.Entity.Input_pin
    enable = lib.Entity.Input_pin
    memory_read = lib.Entity.Output_pin
    memory_write = lib.Entity.Output_pin
    data_program = lib.Entity.Input_pin
    data_memory_in = lib.Entity.Input_pin
    data_memory_out = lib.Entity.Output_pin
    address_program = lib.Entity.Output_pin
    address_memory = lib.Entity.Output_pin

    stage_wb_data_destination = lib.Entity.Output_pin # Check internal signal

    instruction_fetch = CPU_STAGE_IF
    instruction_decode = CPU_STAGE_ID
    execute = CPU_STAGE_EX
    memory_access = CPU_STAGE_MEM
    write_back = CPU_STAGE_WB
    branch_forwarding_unit = CPU_BRANCH_FORWARDING_UNIT
    execution_forwarding_unit = CPU_EXECUTION_FORWARDING_UNIT
    control_hazzard_unit = CPU_HAZZARD_CONTROL_UNIT
   


@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_ADDI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_ADDI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "00000000000000000000000000000010",
        "00000000000000000000000000000100",
        "00000000000000000000000000001000",
        "00000000000000000000000000010000",
        "00000000000000000000000000100000",
        "00000000000000000000000001000000",
        "00000000000000000000000010000000",
        "00000000000000000000000100000000",
        "00000000000000000000000100000001",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_ADD(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_ADD.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000010000",
        "00000000000000000000000000010000",
        "00000000000000000000000000000000",
        "00000000000000000000000000010000",
        "00000000000000000000000000010000",
        "00000000000000000000000000010000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SUB(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SUB.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000010",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000110",
        "00000000000000000000000000000100",
        "00000000000000000000000000000010",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_BEQ(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_BEQ.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000010",
        "00000000000000000000000000000001",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_BNE(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_BNE.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000010",
        "00000000000000000000000000000001",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000011",
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_BLT(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_BLT.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000010",
        "00000000000000000000000000000001",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000011",
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_BLTU(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_BLTU.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000010",
        "00000000000000000000000000000001",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000011",
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_BGE(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_BGE.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000010",
        "00000000000000000000000000000001",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000011",
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_BGEU(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_BGEU.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000010",
        "00000000000000000000000000000001",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000111",
        "00000000000000000000000000000011",
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_LUI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_LUI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000001000000000000",
        "00000000000000000001000000000000",
        "00000000000000000001000000000000",
        "00000000000000000001000000000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_AUIPC(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_AUIPC.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000001000000000100",
        "00000000000000000001000000001000",
        "00000000000000000001000000001100",
        "00000000000000000001000000010000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SLT(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SLT.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "01000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000111",
        "00000000000000000000000000001001",
        "10000000000000000000000000000000",
        "00000000000000000000000000000001",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "00000000000000000000000000000001",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SLTI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SLTI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "10000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "01000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "00000000000000000000000000000001",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SLTU(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SLTU.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "01000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000111",
        "00000000000000000000000000001001",
        "10000000000000000000000000000000",
        "00000000000000000000000000000001",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "00000000000000000000000000000001",
        "00000000000000000000000000000001",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SLTIU(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SLTIU.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "10000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "01000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000001",
        "00000000000000000000000000000001",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_JAL(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_JAL.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
        "00000000000000000000000000010001",
        "00000000000000000000000000011100",
        "00000000000000000000000000000000",
        "00000000000000000000000000001100",
        "00000000000000000000000000010000",
        "00000000000000000000000000010001",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_JALR(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_JALR.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "00000000000000000000000000001000",
        "00000000000000000000000000010000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000010100",
        "00000000000000000000000000000000",
        "00000000000000000000000000100000",
        "00000000000000000000000000000000",
        "00000000000000000000000000100000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        if index == len(values_destination):
            break

        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_LB(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_LB.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000010000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "11111111111111111111111110000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "11111111111111111111111110000010",
        "00000000000000000000000000000000",
    ]

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        if index == len(values_destination):
            break

        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_LBU(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_LBU.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000010000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000010000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000010000010",
        "00000000000000000000000000000000",
    ]

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_LH(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_LH.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000001000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "11111111111111111000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "11111111111111111000000000000010",
        "00000000000000000000000000000000",
    ]

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_LHU(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_LHU.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000001000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000001000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000001000000000000010",
        "00000000000000000000000000000000",
    ]

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_LW(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_LW.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001100",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000010000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001100",
        "00000000000000000000000000010000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001100",
        "00000000000000000000000000010000",
        "00000000000000000000000000000000",
    ]

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        print(f"Clock {index}:")
        print(f"  Fetch Stage: PC = {dut.instruction_fetch.address_program}")


        print(f"  Decode Stage: ULA Data 1= {dut.execute.module_execution_unit.source_1}")
        print(f"  Decode Stage: ULA Data 2= {dut.execute.module_execution_unit.source_2}")
        print(f"  Decode Stage: Data Imediate = {dut.execute.module_execution_unit.immediate}")
        print(f"  Decode Stage: Data Destination = {dut.execute.module_execution_unit.destination}")


        print(f"  Memory Stage: Memory Address = {dut.memory_access}")
        print(f"  Write-Back Stage: WB Data = {dut.stage_wb_data_destination}")
        print(f"  Branch Forwarding Unit: {dut.branch_forwarding_unit}")
        print(f"  Execution Forwarding Unit: {dut.execution_forwarding_unit}")
        print(f"  Control Hazard Unit: {dut.control_hazzard_unit}")
        print(f"  Expected: {values_destination[index]}, got: {dut.stage_wb_data_destination}")

        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_XOR(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_XOR.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "11111111111000000000000000000000",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_XORI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_XORI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "11111111111000000000000000000000",
        "11111111111000000000000000000111",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_AND(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_AND.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "00000000000000000000000000000110",
        "00000000000000000000000000000101",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000110",
        "00000000000000000000000000000101",
        "00000000000000000000000000000100",
        "00000000000000000000000000000101",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_ANDI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_ANDI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "00000000000000000000000000000110",
        "00000000000000000000000000000101",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_OR(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_OR.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "11111111111000000000000000000000",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_ORI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_ORI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "11111111111000000000000000000000",
        "11111111111000000000000000000111",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SLL(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SLL.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000000000100000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000100000000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SLLI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SLLI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000010000000",
        "00000000000000000000000010000000",
        "00000000000000000000000000000000",
        "00000000000000000000000010000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SRL(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SRL.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000100000000",
        "00000000000000000000000000000110",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000100",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SRLI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SRLI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000100000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SRA(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SRA.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000100000000",
        "00000000000000000000000000000110",
        "00000000000000000000000000000100",
        "00000000000000000001000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000001000000",
        "10000000000000000000000000000000",
        "11111110000000000000000000000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SRAI(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SRAI.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000100000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000100",
        "00000000000000000001000000000000",
        "00000000000000000000000001000000",
        "00000000000000000000000001000000",
        "10000000000000000000000000000000",
        "11111110000000000000000000000000",
        "11111110000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000001000000",
        "11111110000000000000000000000000",
        "00000000000000000000000000000000",
    ]

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SB(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SB.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000001001111111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000000000000001111111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000010000001",
        "00000000000000000000000000000000",
    ]

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SH(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SH.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000011000000000000000",
        "00000000000000000000000000001000",
        "00000000000000011000001001111111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000001000001001111111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000001000001010000001",
        "00000000000000000000000000000000",
    ]

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_SW(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_SW.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001000",
        "00000000000000000000000000001000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000001010",
        "00000000000000000000000000000000",
    ]

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
                # Print each step in the pipeline
        print(f"Clock {index}:")
        print(f"  Fetch Stage: Instruction = {dut.instruction_fetch.program_counter.destination}")
        print(f"  Decode Stage: Data Destination = {dut.instruction_decode.data_destination}")

        print(f"  Memory Stage: Memory Address = {dut.memory_access}")
        print(f"  Write-Back Stage: WB Data = {dut.stage_wb_data_destination}")
        print(f"  Branch Forwarding Unit: {dut.branch_forwarding_unit}")
        print(f"  Execution Forwarding Unit: {dut.execution_forwarding_unit}")
        print(f"  Control Hazard Unit: {dut.control_hazzard_unit}")
        print(f"  Expected: {values_destination[index]}, got: {dut.stage_wb_data_destination}")
        yield trace.check(dut.stage_wb_data_destination, values_destination[index], f"At clock {index} (PC = {address}).")


@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_HAZARD_STALL(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/c/blink.s", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",  
        "00000000000000000000000000000100",
        "00000000000000000000000000000100",
        "00000000000000000000000000000100",  
        "00000000000000000000000000000000",
        "00000000000000000000000000000100",
        "00000000000000000000000000000000", 
        "00000000000000000000000000000001",  
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000", #segundo ciclo de stall? porque? a resposta 
        "00000000000000000000000000000100",
        "00000000000000000000000000000000",   
        "00000000000000000000000000001010",  
        "00000000000000000000000000000000",  
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",  
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",  
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",


    ]
    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        # if index >= len(values_destination):
        #     break

        # Print each step in the pipeline
        print(f"Clock {index}:")
        print(f"  Fetch Stage: PC = {dut.instruction_fetch.program_counter.destination}")
        print (f"  Fetch Stage: AdressJump = {dut.instruction_fetch.address_jump}")
        print(f"  Fetch Stage: Enable = {dut.instruction_fetch.enable}")
        print(f"  Fetch Stage: MSource1 = {dut.instruction_fetch.program_counter.mux_source.source_1}")
        print(f"  Fetch Stage: MSource2 = {dut.instruction_fetch.program_counter.mux_source.source_2}")
        print(f"  Fetch Stage: MSelector = {dut.instruction_fetch.program_counter.mux_source.selector}")
        print(f"  Fetch Stage: Mdestination = {dut.instruction_fetch.program_counter.mux_source.destination}")




        print(f" Branch Compare Unit: {dut.instruction_decode.branch_compare_unit.destination}")
        print(f"  Decode Stage: Branch Unit = {dut.instruction_decode.branch_unit.destination}")
        print(f"  Decode Stage: ENABLE = {dut.instruction_decode.enable}")
        print(f"  Decode Stage: Data source 1 = {dut.instruction_decode.module_register_file.data_source_1}")

        print(f"  EXEC Stage: ULA Data 1= {dut.execute.module_execution_unit.source_1}")
        print(f"  EXEC Stage: ULA Data 2= {dut.execute.module_execution_unit.source_2}")
        print(f"  EXEC Stage: Data Imediate = {dut.execute.module_execution_unit.immediate}")
        print(f"  EXEC Stage: Data Destination = {dut.execute.module_execution_unit.destination}")

        print(f"  Memory Stage: Memory Address = {dut.memory_access}")
        print(f"  Write-Back Stage: WB Data = {dut.stage_wb_data_destination}")
        print(f"  Branch Forwarding Unit: {dut.branch_forwarding_unit}")
        print(f"  Execution Forwarding Unit: {dut.execution_forwarding_unit}")
        print(f"  Control Hazard Unit: {dut.control_hazzard_unit}")

        yield 1
    
@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_HAZARD_FORWARDING(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/testcase_HAZARD_FORWARDING.S", stepping=True)
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000011",
        "00000000000000000000000000000110",
        "00000000000000000000000000001001",
        "00000000000000000000000000001111",
        "00000000000000000000000000001111",
        "00000000000000000000000000000110",
        "00000000000000000000000000000000",
        "00000000000000000000000000001001",
        "00000000000000000000000000000000" ,
        "00000000000000000000000000000000",
        "00000000000000000000000000000000"  
          

    ]
    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)

    trace.set_scale(2)

    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        # if index >= len(values_destination):
        #     break

        # Print each step in the pipeline
        print(f"Clock {index}:")
        print(f"  Fetch Stage: PC = {dut.instruction_fetch.address_program}")


        print(f"  Decode Stage: ULA Data 1= {dut.execute.module_execution_unit.source_1}")
        print(f"  Decode Stage: ULA Data 2= {dut.execute.module_execution_unit.source_2}")
        print(f"  Decode Stage: Data Imediate = {dut.execute.module_execution_unit.immediate}")
        print(f"  Decode Stage: Data Destination = {dut.execute.module_execution_unit.destination}")


        print(f"  Memory Stage: Memory Address = {dut.memory_access}")
        print(f"  Write-Back Stage: WB Data = {dut.stage_wb_data_destination}")
        print(f"  Branch Forwarding Unit: {dut.branch_forwarding_unit}")
        print(f"  Execution Forwarding Unit: {dut.execution_forwarding_unit}")
        print(f"  Control Hazard Unit: {dut.control_hazzard_unit}")
        print(f"  Expected: {values_destination[index]}, got: {dut.stage_wb_data_destination}")

        yield trace.check(1, 1, f"At clock {index} (PC = {address}).")

@CPU_TOP_LEVEL.testcase
async def tb_CPU_TOP_LEVEL_C_Code(dut: CPU_TOP_LEVEL, trace: lib.Waveform):
    program = lib.Program("../data/assembly/multply.s", stepping=True)

    # carregar memória esperada de um arquivo
    memory_in = read_expected_memory_dict("../data/c/multply.txt")

    program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    
    trace.set_scale(2)
    


    async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
        if(dut.memory_write == 1):
            pass
    print(program.memory)
    test_in_out_rom(memory_in, program.memory)
    yield True



@pytest.mark.synthesis
def test_CPU_TOP_LEVEL_synthesis():
    CPU_TOP_LEVEL.build_vhd()
    CPU_TOP_LEVEL.build_netlistsvg()

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_hazard_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_HAZARD_FORWARDING)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_HAZARD_STALL)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_hazard_fowarding_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_HAZARD_FORWARDING)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_hazard_stall_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_HAZARD_STALL)


@pytest.mark.testcases
def test_CPU_TOP_LEVEL_arithmetic_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_ADDI)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_ADD)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SUB)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_branch_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_BEQ)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_BNE)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_BLT)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_BLTU)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_BGE)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_BGEU)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_build_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_LUI)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_AUIPC)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_compare_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SLT)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SLTI)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SLTU)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SLTIU)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_jump_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_JAL)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_JALR)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_load_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_LB)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_LBU)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_LH)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_LHU)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_LW)


@pytest.mark.testcases
def test_CPU_TOP_LEVEL_logical_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_XOR)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_XORI)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_AND)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_ANDI)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_OR)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_ORI)

pytest.mark.testcases
def test_CPU_TOP_LEVEL_shifting_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SLL)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SLLI)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SRL)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SRLI)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SRA)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SRAI)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_store_testcases():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SB)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SH)
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_SW)

@pytest.mark.testcases
def test_CPU_TOP_LEVEL_C():
    CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_C_Code)

if __name__ == "__main__":
    lib.run_test(__file__)