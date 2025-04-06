library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

library WORK;

entity MODULE_Branch_Predictor is
    generic (
        DATA_WIDTH  : natural := WORK.RV32I.XLEN;
        BHT_SIZE    : natural := 16  -- Number of entries in the Branch History Table
    );
    port (
        clock        : in  std_logic;
        clear        : in  std_logic;
        enable       : in  std_logic;
        pc_address   : in  std_logic_vector(DATA_WIDTH-1 downto 0); -- PC Address for indexing
        taken        : in  std_logic;  -- Actual branch outcome
        prediction   : out std_logic   -- Predicted outcome
    );
end entity;

architecture RV32I of MODULE_Branch_Predictor is

    type BHT_Array is array (0 to BHT_SIZE-1) of std_logic_vector(1 downto 0);
    signal BHT : BHT_Array := (others => "10"); -- Initializing with weakly taken

    signal index : integer range 0 to BHT_SIZE-1;

begin
    
    index <= to_integer(unsigned(pc_address(DATA_WIDTH-1 downto DATA_WIDTH-4)));
    prediction <= BHT(index)(1); -- MSB of 2-bit counter predicts taken/not taken
    

    
end architecture;
