// Draws a rectangle at the top-left corner of the screen.
// The rectangle is 16 pixels wide and R0 pixels high.
   @0
   D=M
   @INFINITE_LOOP
   D;JLE            // if R0 <= 0 skip drawing
   @countera
   M=D              // counter = R0
   @SCREEN
   D=A
   @address
   M=D              // address = start of screen
(LOOP)
   @address
   A=M
   M=-1             // blacken one row (16 pixels)
   @address
   D=M
   @32
   D=D+A
   @address
   M=D              // address += 32 (next row)
   @counter
   MD=M-1
   @LOOP
   D;JGT            // repeat while counter > 0
(INFINITE_LOOP)
   @INFINITE_LOOP
   0;JMP
