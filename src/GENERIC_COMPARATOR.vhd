library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

library WORK;
use WORK.GENERICS.all;
entity GENERIC_COMPARATOR is
    generic (
        DATA_WIDTH : natural := 8
    );
    port (
        source_1      : in  std_logic_vector(DATA_WIDTH-1 downto 0);
        source_2      : in  std_logic_vector(DATA_WIDTH-1 downto 0);
        flag_equal    : out std_logic;
        flag_less     : out std_logic;
        flag_greater  : out std_logic
    );
end entity;

architecture RTL of GENERIC_COMPARATOR is
    signal signed_1 : signed(DATA_WIDTH-1 downto 0);
    signal signed_2 : signed(DATA_WIDTH-1 downto 0);
begin
    signed_1 <= signed(source_1);
    signed_2 <= signed(source_2);

    flag_equal   <= '1' when signed_1 = signed_2 else '0';
    flag_less    <= '1' when signed_1 < signed_2 else '0';
    flag_greater <= '1' when signed_1 > signed_2 else '0';
end architecture;
