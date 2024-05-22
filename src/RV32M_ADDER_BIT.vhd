library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity RV32M_ALU_BIT is

    port (
        invert_source_2 : in  std_ulogic;
        carry_in        : in  std_ulogic;
        source_1        : in  std_ulogic;
        source_2        : in  std_ulogic;
        destination     : out std_ulogic;
        carry_out       : out std_ulogic
    );

end entity;

architecture RTL of RV32M_ALU_BIT is

    signal source_2_auxiliar : std_ulogic;
    signal half_add          : std_ulogic;
    signal full_add          : std_ulogic;
    signal carry_auxiliar    : std_ulogic;

begin

    source_2_auxiliar <= source_2 XOR invert_source_2;
    carry_auxiliar    <= (source_1 AND source_2_auxiliar) OR (half_add AND carry_in);

    half_add <= source_1 XOR source_2_auxiliar;
    full_add <= half_add XOR carry_in;

    destination <= full_add;
    carry_out   <= carry_auxiliar;

end architecture;
