import sys
import os

# Personal number K = 41 (41 mod 3 = 2 -> duplicate label warning)
K = 41

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "A+D": "0000010",
    "D+M": "1000010", "M+D": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "A&D": "0000000",
    "D&M": "1000000", "M&D": "1000000",
    "D|A": "0010101", "A|D": "0010101",
    "D|M": "1010101", "M|D": "1010101"
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def init_symbols():
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }
    for i in range(16):
        symbols[f"R{i}"] = i
    return symbols

def clean_line(raw_line):
    return raw_line.split("//")[0].strip()

def assemble(asm_path):
    symbols = init_symbols()
    cleaned_instructions = []

    with open(asm_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # Pass 1: Record label addresses and warn on duplicate labels (K mod 3 == 2)
    rom_address = 0
    for line_num, raw in enumerate(raw_lines, start=1):
        line = clean_line(raw)
        if not line:
            continue

        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            if label in symbols:
                print(f"Warning (Line {line_num}): Label '{label}' is written more than once.")
            else:
                symbols[label] = rom_address
        else:
            cleaned_instructions.append((line_num, line))
            rom_address += 1

    # Pass 2: Translate instructions into 16-bit binary
    next_var_address = 16
    binary_output = []

    for line_num, inst in cleaned_instructions:
        if inst.startswith("@"):
            symbol = inst[1:].strip()
            if symbol.isdigit():
                val = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_var_address
                    next_var_address += 1
                val = symbols[symbol]
            binary_output.append(f"0{val:015b}")
        else:
            dest_part, comp_part, jump_part = "", inst, ""
            if "=" in comp_part:
                dest_part, comp_part = comp_part.split("=", 1)
            if ";" in comp_part:
                comp_part, jump_part = comp_part.split(";", 1)

            dest_part = dest_part.strip()
            comp_part = comp_part.strip()
            jump_part = jump_part.strip()

            c_bits = COMP_TABLE[comp_part]
            d_bits = DEST_TABLE[dest_part]
            j_bits = JUMP_TABLE[jump_part]
            binary_output.append(f"111{c_bits}{d_bits}{j_bits}")

    hack_path = os.path.splitext(asm_path)[0] + ".hack"
    with open(hack_path, "w", encoding="utf-8") as f:
        f.write("\n".join(binary_output) + "\n")
    print(f"Successfully assembled {asm_path} -> {hack_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)
    assemble(sys.argv[1])
