import os

import pytest
import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock

from utils_interpreter import *
from utils_GENERIC_ROM import *

import utils
from test_GENERIC_ROM import GENERIC_ROM
from test_GENERIC_RAM import GENERIC_RAM
from test_CPU_TOP_LEVEL import CPU_TOP_LEVEL


class TOP_LEVEL(utils.DUT):
    clock = utils.DUT.Input_pin
    sw = utils.DUT.Input_pin
    led = utils.DUT.Output_pin

    rom = GENERIC_ROM
    ram = GENERIC_RAM
    cpu = CPU_TOP_LEVEL

@TOP_LEVEL.testcase
async def tb_TOP_LEVEL_XOR(dut: TOP_LEVEL, trace: utils.Trace):
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
        "00000000000000000000000000000111",
        "11111111111000000000000000000000",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
    ]

    clock = Clock(dut.clock, 2_000_000_000, units="fs")

    await cocotb.start(clock.start(start_high=False))

    for index, (destination, ) in enumerate(
        zip(values_destination)
    ):

        await trace.cycle()
        yield trace.check(dut.cpu.write_back.destination, destination, f"At clock {index}.")

@TOP_LEVEL.testcase
async def tb_TOP_LEVEL_XORI(dut: TOP_LEVEL, trace: utils.Trace):
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
        "11111111111000000000000000000000",
        "11111111111000000000000000000111",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "11111111111000000000000000000111",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
    ]

    clock = Clock(dut.clock, 2_000_000_000, units="fs")

    await cocotb.start(clock.start(start_high=False))

    for index, (destination, ) in enumerate(
        zip(values_destination)
    ):

        await trace.cycle()
        yield trace.check(dut.cpu.write_back.destination, destination, f"At clock {index}.")

@TOP_LEVEL.testcase
async def tb_TOP_LEVEL_AND(dut: TOP_LEVEL, trace: utils.Trace):
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
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
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
    ]

    clock = Clock(dut.clock, 2_000_000_000, units="fs")

    await cocotb.start(clock.start(start_high=False))

    for index, (destination, ) in enumerate(
        zip(values_destination)
    ):

        await trace.cycle()
        yield trace.check(dut.cpu.write_back.destination, destination, f"At clock {index}.")

@TOP_LEVEL.testcase
async def tb_TOP_LEVEL_ANDI(dut: TOP_LEVEL, trace: utils.Trace):
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
        "00000000000000000000000000000111",
        "00000000000000000000000000000110",
        "00000000000000000000000000000101",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
    ]

    clock = Clock(dut.clock, 2_000_000_000, units="fs")

    await cocotb.start(clock.start(start_high=False))

    for index, (destination, ) in enumerate(
        zip(values_destination)
    ):

        await trace.cycle()
        yield trace.check(dut.cpu.write_back.destination, destination, f"At clock {index}.")

@TOP_LEVEL.testcase
async def tb_TOP_LEVEL_OR(dut: TOP_LEVEL, trace: utils.Trace):
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
        "00000000000000000000000000000111",
        "11111111111000000000000000000000",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "00000000000000000000000000000111",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
    ]

    clock = Clock(dut.clock, 2_000_000_000, units="fs")

    await cocotb.start(clock.start(start_high=False))

    for index, (destination, ) in enumerate(
        zip(values_destination)
    ):

        await trace.cycle()
        yield trace.check(dut.cpu.write_back.destination, destination, f"At clock {index}.")

@TOP_LEVEL.testcase
async def tb_TOP_LEVEL_ORI(dut: TOP_LEVEL, trace: utils.Trace):
    values_destination = [
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
        "11111111111000000000000000000000",
        "11111111111000000000000000000111",
        "11111111111000000000000000000111",
        "00000000000000000000000000000000",
        "11111111111000000000000000000111",
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
    ]

    clock = Clock(dut.clock, 2_000_000_000, units="fs")

    await cocotb.start(clock.start(start_high=False))

    for index, (destination, ) in enumerate(
        zip(values_destination)
    ):

        await trace.cycle()
        yield trace.check(dut.cpu.write_back.destination, destination, f"At clock {index}.")

@pytest.mark.testcases
def test_TOP_LEVEL_LOGICAL_INSTRUCTIONS_testcases():
    memory = "./src/GENERIC_ROM.vhd"

    assembly = "./src/RV32I_INSTRUCTIONS/LOGICAL_INSTRUCTION_AND.asm"
    create_binary_instructions(assembly, memory, instruction_opcode, instruction_funct3, instruction_funct7, instruction_type)
    TOP_LEVEL.build_vhd()
    TOP_LEVEL.test_with(
        testcase=[
            tb_TOP_LEVEL_AND
        ],
    )

    assembly = "./src/RV32I_INSTRUCTIONS/LOGICAL_INSTRUCTION_ANDI.asm"
    create_binary_instructions(assembly, memory, instruction_opcode, instruction_funct3, instruction_funct7, instruction_type)
    TOP_LEVEL.build_vhd()
    TOP_LEVEL.test_with(
        testcase=[
            tb_TOP_LEVEL_ANDI
        ],
    )

    assembly = "./src/RV32I_INSTRUCTIONS/LOGICAL_INSTRUCTION_OR.asm"
    create_binary_instructions(assembly, memory, instruction_opcode, instruction_funct3, instruction_funct7, instruction_type)
    TOP_LEVEL.build_vhd()
    TOP_LEVEL.test_with(
        testcase=[
            tb_TOP_LEVEL_OR
        ],
    )

    assembly = "./src/RV32I_INSTRUCTIONS/LOGICAL_INSTRUCTION_ORI.asm"
    create_binary_instructions(assembly, memory, instruction_opcode, instruction_funct3, instruction_funct7, instruction_type)
    TOP_LEVEL.build_vhd()
    TOP_LEVEL.test_with(
        testcase=[
            tb_TOP_LEVEL_ORI
        ],
    )

    assembly = "./src/RV32I_INSTRUCTIONS/LOGICAL_INSTRUCTION_XOR.asm"
    create_binary_instructions(assembly, memory, instruction_opcode, instruction_funct3, instruction_funct7, instruction_type)
    TOP_LEVEL.build_vhd()
    TOP_LEVEL.test_with(
        testcase=[
            tb_TOP_LEVEL_XOR
        ],
    )

    assembly = "./src/RV32I_INSTRUCTIONS/LOGICAL_INSTRUCTION_XORI.asm"
    create_binary_instructions(assembly, memory, instruction_opcode, instruction_funct3, instruction_funct7, instruction_type)
    TOP_LEVEL.build_vhd()
    TOP_LEVEL.test_with(
        testcase=[
            tb_TOP_LEVEL_XORI
        ],
    )

    create_GENERIC_ROM(memory)   

if __name__ == "__main__":
    pytest.main(["-k", os.path.basename(__file__)])