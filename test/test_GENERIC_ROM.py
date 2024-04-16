import os

import pytest
from cocotb.binary import BinaryValue

import utils
from test_GENERICS_package import GENERICS


class GENERIC_ROM(utils.DUT):
    _package = GENERICS

    address = utils.DUT.Input_pin
    destination = utils.DUT.Output_pin


@GENERIC_ROM.testcase
async def tb_GENERIC_ROM_case_1(dut: GENERIC_ROM, trace: utils.Trace):
    dut.address.value = BinaryValue("00000000")

    await trace.cycle()
    yield trace.check(dut.destination, "00000001")


@pytest.mark.synthesis
def test_GENERIC_ROM_synthesis():
    GENERIC_ROM.build_vhd()
    # GENERIC_ROM.build_netlistsvg()


@pytest.mark.testcases
def test_GENERIC_ROM_testcases():
    GENERIC_ROM.test_with(
        [
            tb_GENERIC_ROM_case_1,
        ]
    )


if __name__ == "__main__":
    pytest.main(["-k", os.path.basename(__file__)])
