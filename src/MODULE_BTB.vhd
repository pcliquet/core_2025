library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity MODULE_BTB is
    Generic (
        NUM_SLOTS   : integer := 16;  -- Number of entries in the BTB
        ADDR_WIDTH : integer := 32 ;  -- Width of addresses
        TAG_WIDTH  : integer :=  ADDR_WIDTH - 4 - 2   -- Width of the tag minus index and offset

    );
    Port (
        clock            : in  std_logic;
        rst              : in  std_logic;
        pc_lookup            : in  std_logic_vector(ADDR_WIDTH-1 downto 0);
        pc_update           : in  std_logic_vector(ADDR_WIDTH-1 downto 0);
        write_en         : in  std_logic;
        branch_taken     : in  std_logic;
        target_addr_in   : in  std_logic_vector(ADDR_WIDTH-1 downto 0);
        target_addr_out  : out std_logic_vector(ADDR_WIDTH-1 downto 0);
        hit              : out std_logic;
        take_branch      : out std_logic;
        tag_out  :         out std_logic_vector(ADDR_WIDTH - 1 downto ADDR_WIDTH - TAG_WIDTH);
        count_out :       out std_logic_vector(1 downto 0);
        index_out :       out integer
    );
end MODULE_BTB;

architecture RV32I of MODULE_BTB is

    constant SLOT_INDEX_WIDTH : integer := 4;
    
    constant SLOT_INDEX_LSB : integer := 2;
    constant SLOT_INDEX_MSB : integer := SLOT_INDEX_WIDTH + SLOT_INDEX_LSB -1;
    
    constant TAG_MSB : integer := ADDR_WIDTH - 1;
    constant TAG_LSB : integer := ADDR_WIDTH - TAG_WIDTH;

    -- Types
    type tag_array is array (0 to NUM_SLOTS-1) of std_logic_vector(TAG_MSB downto TAG_LSB);
    type addr_array     is array (0 to NUM_SLOTS-1) of std_logic_vector(ADDR_WIDTH-1 downto 0);
    type counter_array  is array (0 to NUM_SLOTS-1) of std_logic_vector(1 downto 0); -- 2-bit counters
    type valid_array    is array (0 to NUM_SLOTS-1) of std_logic;

    -- Tables
    signal tag_table      : tag_array     := (others => (others => '0'));
    signal addr_table     : addr_array    := (others => (others => '0'));
    signal counter_table  : counter_array := (others => "01");
    signal valid_table    : valid_array   := (others => '0');

begin

    process (clock, rst)
        variable SLOT_index_update : integer range 0 to NUM_SLOTS-1;
        variable SLOT_index_lookup : integer range 0 to NUM_SLOTS-1;

        variable tag_update      : std_logic_vector(TAG_MSB downto TAG_LSB);
        variable tag_lookup : std_logic_vector(TAG_MSB downto TAG_LSB);
    begin
        if rst = '1' then
            tag_table       <= (others => (others => '0'));
            addr_table      <= (others => (others => '0'));
            counter_table <= (others => "01");
            valid_table     <= (others => '0');
            target_addr_out <= (others => '0');
            hit             <= '0';
            take_branch     <= '0';

        elsif rising_edge(clock) then
            -- Extract index and tag

            SLOT_index_lookup := to_integer(unsigned(pc_lookup(SLOT_INDEX_MSB downto SLOT_INDEX_LSB)));
            tag_lookup := pc_lookup(TAG_MSB downto TAG_LSB);
            SLOT_index_update := to_integer(unsigned(pc_update(SLOT_INDEX_MSB downto SLOT_INDEX_LSB)));
            tag_update := pc_update(TAG_MSB downto TAG_LSB);

            -- Output the tag for debugging
            index_out <= SLOT_index_lookup;
            tag_out <= tag_lookup;
            -- BTB Lookup


            -- Write entry if enabled
            if write_en = '1' then
                if tag_table(SLOT_index_update) /= tag_update or valid_table(SLOT_index_update) = '0' then
                    tag_table(SLOT_index_update)      <= tag_update;
                    addr_table(SLOT_index_update)     <= target_addr_in;
                    valid_table(SLOT_index_update)    <= '1';
                    counter_table(SLOT_index_update)  <= "01";  -- Initialize to weakly taken
                end if;
            end if;

            -- Update prediction counter
            if valid_table(SLOT_index_update) = '1' and tag_table(SLOT_index_update) = tag_update then

                if branch_taken = '1' then
                    case counter_table(SLOT_index_update) is
                        when "00" => counter_table(SLOT_index_update) <= "01";
                        when "01" => counter_table(SLOT_index_update) <= "10";
                        when "10" => counter_table(SLOT_index_update) <= "11";
                        when others => null;
                    end case;
                else
                    case counter_table(SLOT_index_update) is
                        when "11" => counter_table(SLOT_index_update) <= "10";
                        when "10" => counter_table(SLOT_index_update) <= "01";
                        when "01" => counter_table(SLOT_index_update) <= "00";
                        when others => null;
                    end case;
                end if;
            end if;
            if valid_table(SLOT_index_lookup) = '1' and tag_table(SLOT_index_lookup) = tag_lookup then
                target_addr_out <= addr_table(SLOT_index_lookup);
                hit <= '1';
                take_branch <= counter_table(SLOT_index_lookup)(1);  -- MSB of counter
            else
                target_addr_out <= (others => '0');
                hit <= '0';
                take_branch <= '0';
            end if;
            count_out <= counter_table(SLOT_index_lookup);
        end if;
    end process;

end architecture;
