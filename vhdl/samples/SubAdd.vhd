--  Hello world program
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
use IEEE.std_logic_unsigned.all;

--  Defines a design entity, without any ports.
entity subadd is
    Generic(
        constant NBITS : integer := 8
    );
    Port (
            A, B : in std_logic_vector(NBITS-1 downto 0);
            O : in std_logic;
            Y : out std_logic_vector(NBITS-1 downto 0);
            Cout : out std_logic
         );
end subadd;

architecture behaviour of subadd is

    component fulladder is
    Port (
            A, B : in std_logic;
            Cin : in std_logic;
            Y : out std_logic;
            Cout : out std_logic
         );
    end component;
    signal s_C : std_logic_vector(NBITS downto 0);
    signal s_B : std_logic_vector(NBITS-1 downto 0);
    
begin
    -- Entry signals
    s_B  <= B when O = '0' else not(B);
    s_C(0) <= '0' when O = '0' else '1';

    -- Generate for NBITS
    gu : for ii in NBITS-1 downto 0 generate
        gut: fulladder port map (A => A(ii), B => s_B(ii), Cin => s_C(ii), Y => Y(ii), Cout => s_C(ii+1));
    end generate;

    Cout <= s_C(NBITS);



end behaviour;
