# Nand2Tetris Capstone Project (K = 41)

## Project Overview
- **Student:** Ananya Panwar
- **Parameter K:** 41
- **Part B Extra Feature (`41 mod 3 = 2`):** Prints a warning message with line number when a duplicate label is defined.
- **Part C Box Configuration:** Starts at row `41` (RAM address `17696`), `20` rows tall × `32` pixels (`2` words) wide.

## Folder Structure
- `Memory.hdl`, `CPU.hdl`, `Computer.hdl` — Hack computer hardware implementation (Part A)
- `assembler.py` — Two-pass Hack assembler in Python with duplicate-label warning (Part B)
- `Box.asm` & `Box.hack` — Interactive keyboard-controlled box drawing program and assembled binary (Part C)
- `screenshots/` — Place your 7 verification screenshots inside this folder before pushing to GitHub
