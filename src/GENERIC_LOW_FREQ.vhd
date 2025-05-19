LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

LIBRARY WORK;

entity GENERIC_LOW_FREQ is

    generic (
        n : natural := 8    -- O valor "n" do n, define a divisão por "2n".
                            -- Ou seja, não metade do perí­odo da frequência de saÃída.

    );

    port(
        clock     : in  std_logic;
		  div_selector: in std_logic_vector(2 downto 0);
        clock_out : out std_logic
    );

end entity;

architecture RTL of GENERIC_LOW_FREQ is

    signal counter : integer := 0;
    signal tick    : std_logic := '0';
    signal n_sel   : integer := n;

begin

    process(clock)
    begin
        if rising_edge(clock) then

            -- Calcula o novo valor de n baseado no seletor
            case div_selector is
                when "000" => n_sel <= n;           -- 1x
                when "001" => n_sel <= n / 2;       -- 1/2x
                when "010" => n_sel <= n / 4;       -- 1/4x
                when "011" => n_sel <= n / 8;
                when "100" => n_sel <= n / 16;
                when "101" => n_sel <= n / 32;
                when "110" => n_sel <= n / 64;
                when others => n_sel <= 1;          -- fallback
            end case;

            -- Divisor
            if counter > n_sel then
                counter <= 0;
                tick <= not tick;
            else
                counter <= counter + 1;
            end if;

        end if;
    end process;

    clock_out <= tick;

end architecture RTL;
