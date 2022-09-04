--  Hello world program
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
use IEEE.std_logic_unsigned.all;

--  Defines a design entity, without any ports.
entity alu is
    generic (
            constant NBITS : integer := 8;
            constant NBITS_NBITTTTT : integer := 8
        );
    Port (
            A, B : in std_logic_vector(NBITS-1 downto 0);
            AA ,BB3B : in std_logic_vector(NBITS-1 downto 0);
            O : in std_logic_vector(3 downto 0);
            Y : out std_logic_vector(NBITS-1 downto 0);
            C : out std_logic
        );
end alu;

architecture behaviour of alu is

    component subadd is
    Generic(
        constant NBITS : integer
    );
    Port (
            A, B : in std_logic_vector(NBITS-1 downto 0);
            O : in std_logic;
            Y : out std_logic_vector(NBITS-1 downto 0);
            Cout : out std_logic
         );
    end component;

    signal s_Y_subadd : std_logic_vector(NBITS-1 downto 0):= (others => '0');
    signal s_C_subadd : std_logic := '0';
    
begin
    ut_suball: subadd 
    generic map (NBITS => NBITS)
    port map (A => A, B => B,  O => O(0), Y => s_Y_subadd, Cout => s_C_subadd);
    
    Y <= s_Y_subadd when O = "0000" else
         s_Y_subadd when O = "0001" else
         (others => '0') ;
    
    C <= s_C_subadd when O = "0000" else
         s_C_subadd when O = "0001" else
         '0' ;
  /* process(A,B,O) */
  /* begin */
  /*     case(O) is */
  /*           when "0000" => -- Addition */
  /*               Y <= s_Y_subadd; */
  /*               C <= s_C_subadd; */
  /*           when "0001" => -- Soustraction */
  /*               Y <= s_Y_subadd; */
  /*               C <= s_C_subadd; */
  /*           when others => */ 
  /*               Y <= (others=>'0'); */
  /*               C <= '0'; */
  /*       end case; */
        
  /* end process; */

end behaviour;
