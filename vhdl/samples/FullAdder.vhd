--  Hello world program
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
use IEEE.std_logic_unsigned.all;

--  Defines a design entity, without any ports.
entity fulladder is
    Port (
            A, B : in std_logic;
            Cin : in std_logic;
            Y : out std_logic;
            Cout : out std_logic
         );
end fulladder;

architecture behaviour of fulladder is

    signal s_X : std_logic := '0';
    
begin

    -- Temporaty Output
    s_X <= A xor B;

    -- Output
    Y <= s_X xor Cin;
    Cout <= (A and B) or (Cin and s_X);

end behaviour;
