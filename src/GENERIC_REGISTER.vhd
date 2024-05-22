library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

library WORK;

entity GENERIC_REGISTER is

    generic (
        DATA_WIDTH : natural := 8
    );

    port (
        clock       : in  std_ulogic;
        clear       : in  std_ulogic;
        enable      : in  std_ulogic;
        source      : in  std_ulogic_vector((DATA_WIDTH - 1) downto 0);
        destination : out std_ulogic_vector((DATA_WIDTH - 1) downto 0) := (others => '0')
    );

end entity;

architecture RTL of GENERIC_REGISTER is

    -- No signals

begin

    UPDATE : process(clock)
    begin
        if (rising_edge(clock)) then
            if (enable = '1') then
                if (clear = '1') then
                    destination <= (others => '0');
                else
                    destination <= source;
                end if;
            end if;
        end if;
    end process;

end architecture;
