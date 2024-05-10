import os

import pytest
from cocotb.binary import BinaryValue

import utils
from test_CPU_package import CPU


class MODULE_STALL_MUX(utils.DUT):
    _package = CPU

    control_ex_in = utils.DUT.Input_pin
    control_mem_in = utils.DUT.Input_pin
    control_wb_in = utils.DUT.Input_pin
    selector = utils.DUT.Input_pin
    control_ex_out = utils.DUT.Output_pin
    control_mem_out = utils.DUT.Output_pin
    control_wb_out = utils.DUT.Output_pin
    

@pytest.mark.synthesis
def test_MODULE_STALL_MUX_synthesis():
    MODULE_STALL_MUX.build_vhd()
    MODULE_STALL_MUX.build_netlistsvg()


if __name__ == "__main__":
    pytest.main(["-k", os.path.basename(__file__)])
