library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

library WORK;

package GENERICS is

    function reduce_or  (l : std_logic_vector) return std_logic;
    function reduce_and (l : std_logic_vector) return std_logic;

end package;

package body GENERICS is

    function reduce_or (l : std_logic_vector) return std_logic is
        variable result : std_logic := '0';
    begin
        for i in l'reverse_range loop
            result := result OR l(i);
        end loop;
        return result;
    end function;

    function reduce_and (l : std_logic_vector) return std_logic is
        variable result : std_logic := '0';
    begin
        for i in l'reverse_range loop
            result := result AND l(i);
        end loop;
        return result;
    end function;

end package body;
