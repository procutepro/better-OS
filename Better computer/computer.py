import pygame
import os
import math

# Window and color settings
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)


def load_program(filename):
    """
    Loads the program instructions from a file.
    Each non-empty line is considered an instruction.
    """
    with open(filename, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def execute_instruction(instruction, ram, drawing_surface, event, instructions):
    tokens = instruction.split()
    if not tokens:
        return (None, None)

    cmd = tokens[0].lower()

    # Clear command: wipe the drawing surface
    if cmd == "clear":
        drawing_surface.fill(BG_COLOR)
        print("Screen cleared.")
        return (None, None)

    # "draw pixel" command
    if cmd == "drawpixel":
        args = tokens
        if len(args) == 1:
            try:
                x = ram[int(args[0])]
                y = ram[int(args[1])]
                drawing_surface.set_at((x, y), (255, 255, 255))
                print(f"Drew white pixel at ({x}, {y})")
            except ValueError:
                print("Error: Invalid arguments for 'draw pixel'")
        elif len(args) == 5:
            try:
                x = int(args[0])
                y = int(args[1])
                r = int(args[2])
                g = int(args[3])
                b = int(args[4])
                drawing_surface.set_at((x, y), (r, g, b))
                print(f"Drew rect at ({x}, {y}) with color ({r}, {g}, {b})")
            except ValueError:
                print("Error: Invalid arguments for 'draw pixel'")
        else:
            print("Error: 'draw pixel' expects 2 or 5 arguments")
        return (None, None)
    
    if cmd == "drawrectwot":
        # Expect 7 arguments (after the command) referencing RAM indices.
        args = tokens[1:]
        if len(args) == 7:
            try:
                x    = ram[int(args[0])]
                y    = ram[int(args[1])]
                sizex = ram[int(args[2])]
                sizey = ram[int(args[3])]
                r    = ram[int(args[4])]
                g    = ram[int(args[5])]
                b    = ram[int(args[6])]
                pygame.draw.rect(drawing_surface, (r, g, b), pygame.Rect(x, y, sizex, sizey))
            except ValueError:
                pass
        return (None, None)

    if cmd == "drawrectwt":
        # Expect 5 arguments (after the command) referencing RAM indices.
        args = tokens[1:]
        if len(args) == 5:
            try:
                x     = ram[int(args[0])]
                y     = ram[int(args[1])]
                sizex = ram[int(args[2])]
                sizey = ram[int(args[3])]
                # Strip any extra whitespace/newlines from the file name.
                file_name = str(ram[int(args[4])]).strip()
                base_path = r"C:\Users\Pratyush\Downloads\pratyushs_files\VS_code\python\network\computer 1\Better computer\hd"
                file_path = os.path.join(base_path, file_name)
                if not os.path.exists(file_path):
                    print(f"Error: file {file_path} not found.")
                    return (None, None)
                texture = pygame.image.load(file_path)
                scaled_texture = pygame.transform.scale(texture, (sizex, sizey))
                drawing_surface.blit(scaled_texture, (x, y))
            except ValueError as e:
                print("Error in drawrectwt:", e)
        return (None, None)

    if cmd == "load":
        if len(tokens) < 3:
            print("Error: 'load' expects 2 arguments")
            return (None, None)
        try:
            addr = int(tokens[1])
            value = tokens[2]
            if tokens[3] == "i":
                value = float(value)
            elif tokens[3] == "s":
                value = value
            if addr >= len(ram):
                ram.extend([0] * (addr - len(ram) + 1))
            ram[addr] = value
            print(f"Loaded {value} into RAM[{addr}]")
        except ValueError:
            print("Error: Invalid arguments for 'load'")
        return (None, None)

    if cmd == "print":
        if len(tokens) < 2:
            print("Error: 'print' expects 1 argument")
            return (None, None)
        try:
            addr = int(tokens[1])
            if addr >= len(ram):
                print(f"Error: Address {addr} out of range")
            else:
                print(ram[addr])
        except ValueError:
            print("Error: Invalid address for 'print'")
        return (None, None)

    if cmd in ["add", "sub", "mul", "div"]:
        if len(tokens) < 4:
            print(f"Error: '{cmd}' expects 3 arguments: dest, src1, src2")
            return (None, None)
        try:
            dest = int(tokens[1])
            src1 = int(tokens[2])
            src2 = int(tokens[3])
            for addr in (dest, src1, src2):
                if addr >= len(ram):
                    ram.extend([0] * (addr - len(ram) + 1))
            if cmd == "add":
                result = ram[src1] + ram[src2]
            elif cmd == "sub":
                result = ram[src1] - ram[src2]
            elif cmd == "mul":
                result = ram[src1] * ram[src2]
            elif cmd == "div":
                if ram[src2] == 0:
                    print("Error: Division by zero")
                    return (None, None)
                result = ram[src1] / ram[src2]
            ram[dest] = result
            print(f"{cmd.upper()} result stored in RAM[{dest}]: {result}")
        except ValueError:
            print(f"Error: Invalid arguments for '{cmd}'")
        return (None, None)

    if cmd in ["sin", "cos", "tan"]:
        if len(tokens) < 3:
            print(f"Error: '{cmd}' expects 2 arguments: dest, src")
            return (None, None)
        try:
            dest = int(tokens[1])
            src = int(tokens[2])
            if src >= len(ram):
                print("Error: Source address out of range")
                return (None, None)
            if cmd == "sin":
                result = math.sin(ram[src])
            elif cmd == "cos":
                result = math.cos(ram[src])
            elif cmd == "tan":
                result = math.tan(ram[src])
            if dest >= len(ram):
                ram.extend([0] * (dest - len(ram) + 1))
            ram[dest] = result
            print(f"{cmd.upper()} result stored in RAM[{dest}]: {result}")
        except ValueError:
            print(f"Error: Invalid arguments for '{cmd}'")
        return (None, None)

    if cmd == "jmp":
        if len(tokens) < 2:
            print("Error: 'jmp' expects 1 argument (line number)")
            return (None, None)
        try:
            line_num = int(tokens[1])
            new_index = line_num - 1
            print(f"Jumping to line {line_num}")
            return (new_index, None)
        except ValueError:
            print("Error: Invalid line number for 'jmp'")
        return (None, None)

    if cmd == "jic":
        # New syntax: jic <r1> <r2> <comp_mode> <jump_line>
        if len(tokens) < 5:
            print("Error: 'jic' expects 4 arguments: r1, r2, comp_mode, jump_line")
            return (None, None)
        try:
            r1 = int(tokens[1])
            r2 = int(tokens[2])
            comp_mode = int(tokens[3])
            jump_line = int(tokens[4])
            if r1 >= len(ram) or r2 >= len(ram):
                print("Error: Address out of range in 'jic'")
                return (None, None)
            condition_met = False
            if comp_mode == 0:  # equal
                condition_met = (ram[r1] == ram[r2])
            elif comp_mode == 1:  # greater
                condition_met = (ram[r1] > ram[r2])
            elif comp_mode == 2:  # smaller
                condition_met = (ram[r1] < ram[r2])
            elif comp_mode == 3:  # not equal
                condition_met = (ram[r1] != ram[r2])
            else:
                print("Error: Invalid comparison mode in 'jic'. Use 0 for equal, 1 for greater, 2 for smaller, 3 for not equal.")
                return (None, None)

            if condition_met:
                new_index = jump_line - 1
                print(f"Condition met; jumping to line {jump_line}")
                return (new_index, None)
            else:
                print("Condition not met; continuing")
                return (None, None)
        except ValueError:
            print("Error: Invalid arguments for 'jic'")
            return (None, None)
    
    if cmd == "getmousepos":
        ram[int(tokens[1])], ram[int(tokens[2])] = pygame.mouse.get_pos() 
    
    if cmd == "hasclicked?":
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ram[int(tokens[1])] = 1
        else:
            ram[int(tokens[1])] = 0
    
    if cmd == "readline":
        f = os.path.join(r"C:\Users\Pratyush\Downloads\pratyushs_files\VS_code\python\network\computer 1\Better computer\hd", ram[int(tokens[1])])
        with open(f) as file:
            lines = file.readlines()
            if tokens[4] == "i":
                ram[int(tokens[3])] = float(lines[int(tokens[2])])
            if tokens[4] == "s":
                ram[int(tokens[3])] = str(lines[int(tokens[2])])
        return (None, None)

    if cmd == "switch":
        # New instruction to switch program files
        if len(tokens) < 2:
            print("Error: 'switch' expects 1 argument: filename")
            return (None, None)
        new_filename = ram[int(tokens[1])]
        new_path = os.path.join("hd", new_filename)
        if not os.path.exists(new_path):
            print(f"Error: file {new_filename} not found in 'hd'")
            return (None, None)
        new_instructions = load_program(new_path)
        print(f"Switched to program file {new_filename}.")
        return (0, new_instructions)

    print(f"Unknown instruction: {instruction}")
    return (None, None)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Python Computer Simulation")
    clock = pygame.time.Clock()

    # Create a drawing surface (initially clear)
    drawing_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    drawing_surface.fill(BG_COLOR)

    # Initialize RAM as a list.
    ram = [0] * 1024

    # Load the program from the hard drive (hd folder)
    program_file = os.path.join(r"C:\Users\Pratyush\Downloads\pratyushs_files\VS_code\python\network\computer 1\Better computer\hd", "boot.txt")
    print(program_file)
    if not os.path.exists(program_file):
        print("Program file not found in 'hd/boot.txt'!")
        instructions = []
    else:
        instructions = load_program(program_file)
        print("Program loaded from 'hd/programs.txt'. Starting execution...")

    instruction_index = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if instruction_index < len(instructions):
            instr = instructions[instruction_index]
            jump_index, new_prog = execute_instruction(instr, ram, drawing_surface, event, instructions)
            if new_prog is not None:
                # Switch to the new program file
                instructions = new_prog
                instruction_index = 0
            elif jump_index is not None:
                instruction_index = jump_index
            else:
                instruction_index += 1

        # Draw the current drawing surface (no text output on the window)
        screen.fill(BG_COLOR)
        screen.blit(drawing_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
