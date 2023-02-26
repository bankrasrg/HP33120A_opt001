About
===

The HP/Agilent/Keysight 33120A is a 15 MHz function / arbitrary waveform generator. It has been discontinued and replaced by more modern/capable products, but is readily available for hobbyists on the second hand market. The function generator featured one option: Option 001 Phase-Lock Assembly. This small add-on adds some nice capabilities to the instrument: an external clock input and output connector on the rear panel for synchronization to a 10 MHz reference clock, phase offset control from the front panel interface or remote interface, simultaneous hardware triggering of multiple instruments, and finally a more stable internal timebase. Some of the units on the second hand market may have this option installed. However, it will be hard to find the add-on to upgrade a unit with this option. This project has been created to make a replica of the Option 001 Phase-Lock Assembly.

Circuit board
===

The circuit board has been created in KiCad 6.0 using the schematic from the Agilent User's and Service Guide (publication 33120-90022, edition 2, March 2002). Components have been positioned to match the component locator diagram on page 34. A few changes have been made compared to the original design due to component availability. The crystal oscillator HTV1611 from Connor-Winfield (U110) has been replaced by a T604-040.0M from the same manufacturer. Due to the lower operating voltage of this VCTCXO, the reference voltage LT1021DCS8-5 from Linear Technology (U111) was replaced by the ADR4533 from Analog Devices. Some of the resistor values have been changed to better match the lower operating voltage and to adjust the voltage control range of the VCTCXO. Although not tested (yet), the circuit board has been designed to allow the components from the original design to the placed.

![Assembled boards](./doc/assembled_boards.png)

Test results
===

After installation of the board and power-up of the instrument, the Phase Menu becomes available in the front-panel menu and a 10 MHz reference signal is available on the output of the board.  

