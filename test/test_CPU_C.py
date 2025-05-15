# import os
# import pytest
# from cocotb.binary import BinaryValue

# import lib
# from test_CPU_package import CPU
# from test_CPU_STAGE_IF import CPU_STAGE_IF
# from test_CPU_STAGE_ID import CPU_STAGE_ID
# from test_CPU_STAGE_EX import CPU_STAGE_EX
# from test_CPU_STAGE_MEM import CPU_STAGE_MEM
# from test_CPU_STAGE_WB import CPU_STAGE_WB
# from test_CPU_BRANCH_FORWARDING_UNIT import CPU_BRANCH_FORWARDING_UNIT
# from test_CPU_EXECUTION_FORWARDING_UNIT import CPU_EXECUTION_FORWARDING_UNIT
# from test_CPU_HAZZARD_CONTROL_UNIT import CPU_HAZZARD_CONTROL_UNIT

# def pytest_addoption(parser):
#     parser.addoption(
#         "--program_name",
#         action="store",
#         default="multply.s",
#         help="Nome do arquivo de programa C a ser testado"
#     )

# @pytest.fixture
# def program_name(request):
#     return request.config.getoption("--program_name")

# def olha_so():
#     while True:
#         nome = input("\nQual nome do file? ") 
#         c = nome +'.c'
#         # Verifique se o arquivo existe na pasta atual
#         if c in os.listdir('./data/c'):  # '.' refere-se à pasta atual
#             break
#         else:
#             print(f"O arquivo '{nome}' não foi encontrado na pasta.")
    
#     return nome


# def read_expected_memory_dict(path):
#     memory = {}
#     with open(path, 'r') as f:
#         for line in f:
#             if ':' in line:
#                 addr, val = line.strip().split(':')
#                 binv = val.strip().replace('"', '').replace(',', '')
#                 memory[int(addr)] = binv.zfill(32)
#     return memory

# def test_in_out_rom(input_mem, output_mem):
#     GREEN, RED, YELLOW, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[0m"

#     for addr in input_mem:
#         if addr not in output_mem:
#             print(f"{YELLOW}address {addr} missing in output{RESET}")
#             continue
#         inp = input_mem[addr].zfill(32)
#         out = output_mem[addr]
#         if inp == out:
#             print(f"{GREEN}match at {addr}: {inp}{RESET}")
#         else:
#             print(f"{RED}mismatch at {addr}{RESET}")
#             print(f"{RED}  input : {inp}{RESET}")
#             print(f"{RED}  output: {out}{RESET}")

# # ---------------------------
# # CLASSE CPU_TOP_LEVEL_C
# # ---------------------------
# class CPU_TOP_LEVEL(lib.Entity):
#     _package = CPU

#     clock = lib.Entity.Input_pin
#     clear = lib.Entity.Input_pin
#     enable = lib.Entity.Input_pin
#     memory_read = lib.Entity.Output_pin
#     memory_write = lib.Entity.Output_pin
#     data_program = lib.Entity.Input_pin
#     data_memory_in = lib.Entity.Input_pin
#     data_memory_out = lib.Entity.Output_pin
#     address_program = lib.Entity.Output_pin
#     address_memory = lib.Entity.Output_pin

#     stage_wb_data_destination = lib.Entity.Output_pin

#     instruction_fetch = CPU_STAGE_IF
#     instruction_decode = CPU_STAGE_ID
#     execute = CPU_STAGE_EX
#     memory_access = CPU_STAGE_MEM
#     write_back = CPU_STAGE_WB
#     branch_forwarding_unit = CPU_BRANCH_FORWARDING_UNIT
#     execution_forwarding_unit = CPU_EXECUTION_FORWARDING_UNIT
#     control_hazzard_unit = CPU_HAZZARD_CONTROL_UNIT


# # ---------------------------
# # TESTBENCH COCOTB
# # ---------------------------
# # @CPU_TOP_LEVEL.testcase
# # async def tb_CPU_TOP_LEVEL_C_Code(dut: CPU_TOP_LEVEL, trace: lib.Waveform, program_name: str):
# #     asm_dir = "../data/assembly/"
# #     file_path = os.path.join(asm_dir, program_name)
# #     if not os.path.exists(file_path):
# #         raise FileNotFoundError(f"Arquivo .s não encontrado: {file_path}")

# #     program = lib.Program(file_path, stepping=True)

# #     txt_path = os.path.join("../data/c/", program_name.replace('.s', '.txt'))
# #     if not os.path.exists(txt_path):
# #         raise FileNotFoundError(f"Arquivo .txt não encontrado: {txt_path}")

# #     mem_in = read_expected_memory_dict(txt_path)
# #     program.attach_memory(
# #         dut.memory_read, dut.memory_write,
# #         dut.address_memory, dut.data_memory_out, dut.data_memory_in
# #     )
# #     trace.set_scale(2)

# #     async for _idx, _addr in program.attach_device(trace, dut.address_program, dut.data_program):
# #         if dut.memory_write == 1:
# #             pass

# #     print(program.memory)
# #     test_in_out_rom(mem_in, program.memory)
# #     yield True
# #nome = olha_so()
# @CPU_TOP_LEVEL.testcase
# async def tb_CPU_TOP_LEVEL_C_Code(dut: CPU_TOP_LEVEL, trace: lib.Waveform, program_name: str):

#     #olha_so()
#     program = lib.Program(f"../data/assembly/{program_name}.s", stepping=True)
#     memory_in = read_expected_memory_dict(f"../data/c/{program_name}.txt")


#     program.attach_memory(dut.memory_read, dut.memory_write, dut.address_memory, dut.data_memory_out, dut.data_memory_in)
    
#     trace.set_scale(2)
    


#     async for index, address in program.attach_device(trace, dut.address_program, dut.data_program):
#         if(dut.memory_write == 1):
#             pass
#     #print(program.memory)
#     print(program_name)
#     test_in_out_rom(memory_in, program.memory)
#     yield True


# # ---------------------------
# # CHAMADA DE TESTE COM PYTEST
# # ---------------------------
# @pytest.mark.testcases
# def test_CPU_TOP_LEVEL_C_Code(program_name = olha_so()):
#     CPU_TOP_LEVEL.test_with(tb_CPU_TOP_LEVEL_C_Code)