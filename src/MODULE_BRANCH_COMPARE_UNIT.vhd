library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

library WORK;

entity MODULE_BRANCH_COMPARE_UNIT is

    generic (
        FUNCTION_WIDTH : natural := WORK.RV32I.FUNCT3_WIDTH + 1;
        DATA_WIDTH     : natural := WORK.RV32I.XLEN
    );

    port (
        enable             : in  std_logic;
        select_function    : in  std_logic_vector((FUNCTION_WIDTH - 1) downto 0);
        source_1           : in  std_logic_vector((DATA_WIDTH - 1) downto 0);
        source_2           : in  std_logic_vector((DATA_WIDTH - 1) downto 0);
        forward            : in  WORK.CPU.t_FORWARD_BRANCH := WORK.CPU.NULL_FORWARD_BRANCH;
        data_source_1      : out std_logic_vector((DATA_WIDTH - 1) downto 0);
        destination        : out std_logic
    );

end entity;

architecture RV32I of MODULE_BRANCH_COMPARE_UNIT is

    alias sign_1 : std_logic is source_1(WORK.RV32I.XLEN - 1);
    alias sign_2 : std_logic is source_2(WORK.RV32I.XLEN - 1);

    signal flag_branch   : std_logic;
    signal flag_equal    : std_logic;
    signal flag_less     : std_logic;
    signal flag_greather : std_logic;

    signal forward_source_1 : std_logic_vector((DATA_WIDTH - 1) downto 0);
    signal forward_source_2 : std_logic_vector((DATA_WIDTH - 1) downto 0);

begin

    destination <= enable AND flag_branch;
    data_source_1 <= forward_source_1;

    MUX_FORWARD_SOURCE_1 : entity WORK.GENERIC_MUX_2X1
        generic map (
            DATA_WIDTH => WORK.RV32I.XLEN
        )
        port map (
            selector    => forward.select_source_1,
            source_1    => source_1,
            source_2    => forward.source_mem,
            destination => forward_source_1
        );

    MUX_FORWARD_SOURCE_2 : entity WORK.GENERIC_MUX_2X1
        generic map (
            DATA_WIDTH => WORK.RV32I.XLEN
        )
        port map (
            selector    => forward.select_source_2,
            source_1    => source_2,
            source_2    => forward.source_mem,
            destination => forward_source_2
        );

    COMPARATOR : entity WORK.GENERIC_COMPARATOR
        generic map (
            DATA_WIDTH => WORK.RV32I.XLEN
        )
        port map (
            source_1      => forward_source_1,
            source_2      => forward_source_2,
            flag_equal    => flag_equal,
            flag_less     => flag_less,
            flag_greater => flag_greather
        );

    CONTROLLER: entity WORK.RV32I_BRANCH_CONTROLLER
        port map (
            select_function => select_function(2 downto 0),
            flag_sign_1     => sign_1,
            flag_sign_2     => sign_2,
            flag_equal      => flag_equal,
            flag_less       => flag_less,
            flag_greather   => flag_greather,
            destination     => flag_branch
        );

end architecture;
