import pytest
import cocotb
import random
from cocotb.binary import BinaryValue
import lib
from test_MODULES_package import MODULES

class MODULE_BTB(lib.Entity):
    _package = MODULES
    clock = lib.Entity.Input_pin
    rst = lib.Entity.Input_pin
    pc_lookup = lib.Entity.Input_pin
    pc_update = lib.Entity.Input_pin
    write_en = lib.Entity.Input_pin
    branch_taken = lib.Entity.Input_pin
    target_addr_in = lib.Entity.Input_pin
    target_addr_out = lib.Entity.Output_pin
    hit = lib.Entity.Output_pin
    take_branch = lib.Entity.Output_pin
    tag_out = lib.Entity.Output_pin
    index_out = lib.Entity.Output_pin
    count_out = lib.Entity.Output_pin


@MODULE_BTB.testcase
async def tb_MODULE_BTB_case_1(dut: MODULE_BTB, trace: lib.Waveform):
    """
    Basic test for BTB:
    - First access (miss)
    - Write entry
    - Second access (hit)
    """

    # Reset the BTB
    dut.rst.value = BinaryValue("1")
    dut.write_en.value = BinaryValue("0")

    await trace.cycle()
    dut.rst.value = BinaryValue("0")
    await trace.cycle()

    # Step 1: Read an address (Miss expected)
    test_pc = "00000000000000000000000000010001"  # Example PC address
    dut.pc_lookup.value = BinaryValue(test_pc)
    await trace.cycle()

    yield trace.check(dut.hit, "0")  # Expect miss
    yield trace.check(dut.target_addr_out, "00000000000000000000000000000000")

    await trace.cycle()

    # Step 2: Write an entry to BTB
    test_target = "00000000000000000000000001000001"  # Example target
    dut.pc_update.value = BinaryValue(test_pc)
    dut.target_addr_in.value = BinaryValue(test_target)
    dut.write_en.value = BinaryValue("1")
    await trace.cycle()

    dut.write_en.value = BinaryValue("0")  # Disable write
    await trace.cycle()

    # Step 3: Read again (Hit expected)
    dut.pc_lookup.value = BinaryValue(test_pc)
    await trace.cycle()

    dut.pc_lookup.value = BinaryValue(test_pc)
    print(dut.hit)
    yield trace.check(dut.hit, "1")  # Expect hit
    yield trace.check(dut.target_addr_out, test_target)
    await trace.cycle()
@MODULE_BTB.testcase
async def tb_btb_write_and_hit(dut: MODULE_BTB, trace: lib.Waveform):
    """Test a correct write and readback hit."""
    dut.rst.value = BinaryValue("1")
    dut.write_en.value = BinaryValue("0")
    await trace.cycle()

    dut.rst.value = BinaryValue("0")
    await trace.cycle()

    pc = "00000000000000000000000000001000"
    target = "00000000000000000000000010101010"

    # Miss expected
    dut.pc_lookup.value = BinaryValue(pc)
    await trace.cycle()
    yield trace.check(dut.hit, "0")

    # Write entry
    dut.pc_update.value = BinaryValue(pc)
    dut.target_addr_in.value = BinaryValue(target)
    dut.write_en.value = BinaryValue("1")
    await trace.cycle()
    dut.pc_update.value = BinaryValue("00000000000000000000000000000000")
    dut.pc_lookup.value = BinaryValue(pc)

    dut.write_en.value = BinaryValue("0")
    await trace.cycle()

    # Hit expected
    dut.pc_lookup.value = BinaryValue("00000000000000000000000000000000")

    await trace.cycle()

    yield trace.check(dut.hit, "1")
    yield trace.check(dut.target_addr_out, target)

@MODULE_BTB.testcase
async def tb_btb_tag_miss(dut: MODULE_BTB, trace: lib.Waveform):
    """Test a tag mismatch resulting in a miss."""
    dut.rst.value = BinaryValue("1")
    await trace.cycle()
    dut.rst.value = BinaryValue("0")

    # Write one entry
    pc = "00000000000000000000000000001111"
    target = "00000000000000000000000011110000"
    dut.pc_update.value = BinaryValue(pc)
    dut.target_addr_in.value = BinaryValue(target)
    dut.write_en.value = BinaryValue("1")
    await trace.cycle()
    dut.write_en.value = BinaryValue("0")
    await trace.cycle()

    # Mismatch tag (same set index)
    mismatching_pc = "00000000000000000000000100001111"
    dut.pc_lookup.value = BinaryValue(mismatching_pc)
    await trace.cycle()
    yield trace.check(dut.hit, "0")
@MODULE_BTB.testcase
async def tb_btb_saturating_counter(dut: MODULE_BTB, trace: lib.Waveform):
    """Test 2-bit saturating counter update and branch prediction."""
    dut.rst.value = BinaryValue("1")
    await trace.cycle()
    dut.rst.value = BinaryValue("0")

    pc = "00000000000000000000000000010101"
    target = "00000000000000000000000001010101"

    # Write to BTB
    dut.pc_update.value = BinaryValue(pc)
    dut.target_addr_in.value = BinaryValue(target)
    dut.write_en.value = BinaryValue("1")
    await trace.cycle()
    dut.write_en.value = BinaryValue("0")

    # Hit: simulate 3 taken branches → counter should saturate to 3
    for _ in range(3):
        dut.pc_lookup.value = BinaryValue(pc)
        dut.branch_taken.value = BinaryValue("1")
        await trace.cycle()

    # Prediction should be taken
    yield trace.check(dut.take_branch, "1")

    # Now simulate 3 not-taken → counter should decrease
    for _ in range(3):
        dut.branch_taken.value = BinaryValue("0")
        await trace.cycle()

    # Prediction should be not taken (counter MSB = 0)
    yield trace.check(dut.take_branch, "0")

@MODULE_BTB.testcase
async def tb_btb_index_collision(dut: MODULE_BTB, trace: lib.Waveform):
    """Test BTB behavior when two PCs with same index but different tags overwrite each other."""

    # Reset
    dut.rst.value = BinaryValue("1")
    await trace.cycle()
    dut.rst.value = BinaryValue("0")

    pc1 = "00000000000000000000000000000000"
    pc2 = "00000000000000010000000000000000"  # Same index, different tag

    target1 = "00000000000000000000000000010000"
    target2 = "00000000000000000000000000100000"

    # Write pc1 -> target1
    dut.pc_update.value = BinaryValue(pc1)
    dut.target_addr_in.value = BinaryValue(target1)
    dut.write_en.value = BinaryValue("1")
    await trace.cycle()

    dut.write_en.value = BinaryValue("0")
    await trace.cycle()

    # Write pc2 -> target2 (overwrite)
    dut.pc_update.value = BinaryValue(pc2)
    dut.target_addr_in.value = BinaryValue(target2)
    dut.write_en.value = BinaryValue("1")
    await trace.cycle()

    dut.write_en.value = BinaryValue("0")
    await trace.cycle()

    # Check if pc1 is now a miss
    dut.pc_lookup.value = BinaryValue(pc1)
    await trace.cycle()
    yield trace.check(dut.hit, "0")

    # Check if pc2 hits
    dut.pc_lookup.value = BinaryValue(pc2)
    await trace.cycle()
    yield trace.check(dut.hit, "1")
    yield trace.check(dut.target_addr_out, target2)


@MODULE_BTB.testcase
async def tb_MODULE_BTB_partial_tag_hit(dut: MODULE_BTB, trace: lib.Waveform):
    """
    Test case where the tag bits match but the full PC address is different.
    This should result in a miss.
    """

    # Reset the BTB
    dut.rst.value = BinaryValue("1")
    dut.write_en.value = BinaryValue("0")
    await trace.cycle()
    dut.rst.value = BinaryValue("0")
    await trace.cycle()

    # Set a PC address to write
    original_pc = "00000000000000000000000000010001"  # PC to write
    target_addr = "00000000000000000000000000011111"  # Target to write

    # Step 1: Write to BTB
    dut.pc_update.value = BinaryValue(original_pc)
    dut.target_addr_in.value = BinaryValue(target_addr)
    dut.write_en.value = BinaryValue("1")
    await trace.cycle()
    dut.write_en.value = BinaryValue("0")
    await trace.cycle()

    # Step 2: Access a different PC that shares the same tag + index
    mismatched_pc = "11110000000000000000000000010001"  # Different upper bits

    dut.pc_lookup.value = BinaryValue(mismatched_pc)
    await trace.cycle()

    # Should miss
    yield trace.check(dut.hit, "0")
    yield trace.check(dut.target_addr_out, "00000000000000000000000000000000")

@MODULE_BTB.testcase
async def tb_btb_take_branch_single_cycle(dut: MODULE_BTB, trace: lib.Waveform):
    """Test if BTB take_branch output updates after one clock when branch is taken."""

    # Reset
    dut.rst.value = BinaryValue("1")
    await trace.cycle()
    dut.rst.value = BinaryValue("0")
    await trace.cycle()

    # Input values
    pc = "00000000000000000000000000010000"        # PC address
    target = "00000000000000000000000000100000"    # Target address

    # Initial write to BTB
    dut.branch_taken.value = BinaryValue("1")  # Simulate a taken branch

    dut.pc_update.value = BinaryValue(pc)
    dut.target_addr_in.value = BinaryValue(target)
    dut.write_en.value = BinaryValue("1")
    await trace.cycle()
    dut.write_en.value = BinaryValue("0")

    # Simulate a taken branch (update counter)
    dut.pc_lookup.value = BinaryValue(pc)
    dut.branch_taken.value = BinaryValue("1")
    await trace.cycle()
    await trace.cycle()


    # Assert take_branch is now '1'
    yield trace.check(dut.take_branch, "1")


@MODULE_BTB.testcase
async def tb_btb_exhaustive(dut: MODULE_BTB, trace: lib.Waveform):
    """Exhaustively test all BTB entries: write, verify hit, test collisions."""

    import random

    # Reset BTB
    dut.rst.value = BinaryValue("1")
    await trace.cycle()
    dut.rst.value = BinaryValue("0")

    NUM_SLOTS = 16
    ADDR_WIDTH = 32

    # Helper to generate PC addresses with same index bits but unique tags
    def make_pc(tag_val, index_val):
        pc = (tag_val << 6) | (index_val << 2)
        return f"{pc:032b}"

    # Step 1: Fill all slots with unique tags and indexes
    for index in range(NUM_SLOTS):
        tag = random.randint(1, 2**(ADDR_WIDTH - 6) - 1)
        pc = make_pc(tag, index)
        target = f"{(index + 1) << 4:032b}"

        # Write
        dut.pc_update.value = BinaryValue(pc)
        dut.target_addr_in.value = BinaryValue(target)
        dut.write_en.value = BinaryValue("1")
        await trace.cycle()
        dut.write_en.value = BinaryValue("0")
        await trace.cycle()

        # Read
        dut.pc_lookup.value = BinaryValue(pc)
        await trace.cycle()
        
        yield trace.check(dut.hit, "1")
        yield trace.check(dut.target_addr_out, target)

    # Step 2: Overwrite every entry with a different tag (same index)
    for index in range(NUM_SLOTS):
        new_tag = random.randint(1, 2**(ADDR_WIDTH - 6) - 1)
        pc_new = make_pc(new_tag, index)
        new_target = f"{(index + 100) << 4:032b}"

        # Write with new tag (overwrite old tag at same index)
        dut.pc_update.value = BinaryValue(pc_new)
        dut.target_addr_in.value = BinaryValue(new_target)
        dut.write_en.value = BinaryValue("1")
        await trace.cycle()
        dut.write_en.value = BinaryValue("0")
        await trace.cycle()

        # Old PC (different tag) should now miss
        pc_old = make_pc(new_tag - 1, index)
        dut.pc_lookup.value = BinaryValue(pc_old)
        await trace.cycle()
        yield trace.check(dut.hit, "0")

        # New PC should hit
        dut.pc_lookup.value = BinaryValue(pc_new)
        await trace.cycle()
        yield trace.check(dut.hit, "1")
        yield trace.check(dut.target_addr_out, new_target)

    # Step 3: Test prediction counter behavior
    for index in range(NUM_SLOTS):
        tag = random.randint(1, 2**(ADDR_WIDTH - 6) - 1)
        pc = make_pc(tag, index)
        target = f"{(index + 200) << 4:032b}"

        # Write entry
        dut.pc_update.value = BinaryValue(pc)
        dut.target_addr_in.value = BinaryValue(target)
        dut.write_en.value = BinaryValue("1")
        await trace.cycle()
        dut.write_en.value = BinaryValue("0")

        # Simulate 3 taken branches to saturate the counter
        dut.pc_lookup.value = BinaryValue(pc)
        for _ in range(3):
            dut.branch_taken.value = BinaryValue("1")
            await trace.cycle()

        # Prediction should now be '1' (strongly taken)
        yield trace.check(dut.take_branch, "1")

        # Simulate 3 not taken to reduce the counter
        for _ in range(3):
            dut.branch_taken.value = BinaryValue("0")
            await trace.cycle()

        # Prediction should now be '0' (not taken)
        yield trace.check(dut.take_branch, "0")


@pytest.mark.synthesis
def test_MODULE_BTB_synthesis():
    MODULE_BTB.build_vhd()
    MODULE_BTB.build_netlistsvg()



@pytest.mark.testcases
def test_MODULE_BTB_case_1():
    MODULE_BTB.test_with(tb_MODULE_BTB_case_1)


@pytest.mark.testcases
def test_MODULE_BTB_write_and_hit():
    MODULE_BTB.test_with(tb_btb_write_and_hit)


@pytest.mark.testcases
def test_MODULE_BTB_tag_miss():
    MODULE_BTB.test_with(tb_btb_tag_miss)


@pytest.mark.testcases
def test_MODULE_BTB_saturating_counter():
    MODULE_BTB.test_with(tb_btb_saturating_counter)


@pytest.mark.testcases
def test_MODULE_BTB_collison():
    MODULE_BTB.test_with(tb_btb_index_collision)

@pytest.mark.testcases
def test_MODULE_BTB_partial_tag_hit():
    MODULE_BTB.test_with(tb_MODULE_BTB_partial_tag_hit)

@pytest.mark.testcases
def test_MODULE_BTB_take_branch_single_cycle():
    MODULE_BTB.test_with(tb_btb_take_branch_single_cycle)

@pytest.mark.testcases
def test_MODULE_BTB_exhaustive():
    MODULE_BTB.test_with(tb_btb_exhaustive)


# Removed the coverage test

if __name__ == "__main__":
    lib.run_test(__file__)
