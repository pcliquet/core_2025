import os

import pytest
from cocotb.binary import BinaryValue

import utils
from test_RV32I_package import RV32I
from test_RV32I_ALU_BIT import RV32I_ALU_BIT


class RV32I_ALU(utils.DUT):
    _package = RV32I

    invert_source_1 = utils.DUT.Input_pin
    invert_source_2 = utils.DUT.Input_pin
    select_function = utils.DUT.Input_pin
    source_1 = utils.DUT.Input_pin
    source_2 = utils.DUT.Input_pin
    destination = utils.DUT.Output_pin

    bit_to_bit = RV32I_ALU_BIT


@RV32I_ALU.testcase
async def tb_RV32I_ALU_case_1(dut: RV32I_ALU, trace: utils.Trace):
    dut.invert_source_1.value = BinaryValue("0")
    dut.invert_source_2.value = BinaryValue("0")
    dut.select_function.value = BinaryValue("000")
    dut.source_1.value = BinaryValue("00000000000000000000000000000000")
    dut.source_2.value = BinaryValue("11111111111111111111111111111111")

    await trace.cycle()
    yield trace.check(dut.destination, "00000000000000000000000000000000")

    dut.select_function.value = BinaryValue("001")
    dut.source_1.value = BinaryValue("11111111111111111111111111111111")
    dut.source_2.value = BinaryValue("00000000000000000000000000000000")

    await trace.cycle()
    yield trace.check(dut.destination, "11111111111111111111111111111111")

    dut.select_function.value = BinaryValue("011")
    dut.source_1.value = BinaryValue("11111111111111110000000000000000")
    dut.source_2.value = BinaryValue("00000000000000001111111111111111")

    await trace.cycle()
    yield trace.check(dut.destination, "11111111111111111111111111111111")

    dut.select_function.value = BinaryValue("110")
    dut.source_1.value = BinaryValue("11111111111111111111111111111111")
    dut.source_2.value = BinaryValue("00000000000000000000000000000000")

    await trace.cycle()
    yield trace.check(dut.destination, "00000000000000000000000000000001")

    dut.invert_source_1.value = BinaryValue("1")
    dut.select_function.value = BinaryValue("000")
    dut.source_1.value = BinaryValue("00000000000000000000000000000000")
    dut.source_2.value = BinaryValue("11111111111111111111111111111111")

    await trace.cycle()
    yield trace.check(dut.destination, "11111111111111111111111111111111")

    dut.invert_source_1.value = BinaryValue("0")
    dut.invert_source_2.value = BinaryValue("1")
    dut.select_function.value = BinaryValue("001")
    dut.source_1.value = BinaryValue("11111111111111111111111111111111")
    dut.source_2.value = BinaryValue("00000000000000000000000000000000")

    await trace.cycle()
    yield trace.check(dut.destination, "11111111111111111111111111111111")

    dut.invert_source_1.value = BinaryValue("1")
    dut.invert_source_2.value = BinaryValue("0")
    dut.select_function.value = BinaryValue("011")
    dut.source_1.value = BinaryValue("11111111111111110000000000000000")
    dut.source_2.value = BinaryValue("11111111111111110000000000000000")

    await trace.cycle()
    yield trace.check(dut.destination, "00000000000000000000000000000000")

    dut.invert_source_1.value = BinaryValue("1")
    dut.invert_source_2.value = BinaryValue("1")
    dut.select_function.value = BinaryValue("100")
    dut.source_1.value = BinaryValue("11111111111111111111111111111111")
    dut.source_2.value = BinaryValue("00000000000000000000000000000000")

    await trace.cycle()
    yield trace.check(dut.destination, "00000000000000000000000000000001")



@pytest.mark.synthesis
def test_RV32I_ALU_synthesis():
    RV32I_ALU.build_vhd()
    # RV32I_ALU.build_netlistsvg()


@pytest.mark.testcases
def test_RV32I_ALU_testcases():
    RV32I_ALU.test_with(
        [
            tb_RV32I_ALU_case_1,
        ]
    )


if __name__ == "__main__":
    pytest.main(["-k", os.path.basename(__file__)])
