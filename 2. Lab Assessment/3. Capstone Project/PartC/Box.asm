// Box.asm for K = 41
// Starts at row 41 (address 16384 + 32*41 = 17696)
// Height = 20 rows, Width = 32 pixels (2 words from left edge)

(LOOP)
    // Poll keyboard (@KBD = 24576)
    @KBD
    D=M
    @SET_WHITE
    D;JEQ           // If no key pressed (KBD == 0), set color = 0

    @color
    M=-1            // Key pressed: set color = -1 (black)
    @DRAW_INIT
    0;JMP

(SET_WHITE)
    @color
    M=0             // Key released: set color = 0 (white)

(DRAW_INIT)
    // Start address = SCREEN (16384) + 32 * 41 = 17696
    @17696
    D=A
    @row_addr
    M=D

    // Box height = 20 rows
    @20
    D=A
    @rows_left
    M=D

(ROW_LOOP)
    @rows_left
    D=M
    @LOOP
    D;JEQ           // Done drawing all 20 rows; return to keyboard check

    @row_addr
    D=M
    @curr_addr
    M=D

    // Box width = (41 mod 4) + 1 = 2 words (32 pixels)
    @2
    D=A
    @cols_left
    M=D

(COL_LOOP)
    @cols_left
    D=M
    @NEXT_ROW
    D;JEQ           // Done drawing 2 words on this row

    @color
    D=M
    @curr_addr
    A=M
    M=D             // Fill 16 pixels with black (-1) or white (0)

    @curr_addr
    M=M+1           // Move right by 1 word (16 pixels)
    @cols_left
    M=M-1
    @COL_LOOP
    0;JMP

(NEXT_ROW)
    @32
    D=A
    @row_addr
    M=D+M           // Move down 1 row (+32 words)

    @rows_left
    M=M-1
    @ROW_LOOP
    0;JMP
