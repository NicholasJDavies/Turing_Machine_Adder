# Author: Nicholas Davies
# run with: python3 ./turing_machine.py
import re
import time

MAX_LOOPS = 1000

# Turing Machine Class
class machine:
    '''
    Recognised Symbols: '1', 'X', ' '

    Instructions:
           -Tape Symbol-
    dial    __  X   1
    1       D6  E2  R1
    2       R2  E3  ? 
    3       R3  E4  E5
    4       L4  ?   R6
    5       L5  ?   R1
    6       X6  !   R3

    Letter Code:
    D = write '1'
    X = write 'X'
    E = clear current symbol
    R = move tape right (head moves left)
    L = move tape left (head moves right)
    ? = error
    ! = halt, successful

    Number (in instruction codes):
        sets dial to number.
    '''

    # Initialises the Turing Machine
    def __init__(self,  tape, position, dial):
        arr = [char for char in tape]
        self.tape = [' ' for i in range(5)] + arr + [' ' for i in range(5)]
        self.position = position + 5
        self.dial = dial

    # The main_loop which will govern the Turing Machine's workflow.
    def main_loop(self, verbose=True):
        output = 0
        loops = 0
        while(output == 0 and loops < MAX_LOOPS):
            if(verbose):
                self.print_state()
            output = self.execute_func()
            loops += 1

    # Instructions of the Turing Machine
    instructions = {
        (' ', 1): ('D', 6),
        (' ', 2): ('R', 2),
        (' ', 3): ('R', 3),
        (' ', 4): ('L', 4),
        (' ', 5): ('L', 5),
        (' ', 6): ('X', 6),

        ('X', 1): ('E', 2),
        ('X', 2): ('E', 3),
        ('X', 3): ('E', 4),
        ('X', 4): ('?', 0),
        ('X', 5): ('?', 0),
        ('X', 6): ('!', 0),

        ('1', 1): ('R', 1),
        ('1', 2): ('?', 1),
        ('1', 3): ('E', 5),
        ('1', 4): ('R', 6),
        ('1', 5): ('R', 1),
        ('1', 6): ('R', 3)
    }

    # returns the current instruction
    def get_code(self):
        code = self.tape[self.position]
        instr = machine.instructions[code, self.dial]
        return instr
        
    # executes function on tape 
    # returns:
    #   "0" if continuing
    #   "1" when done (no errors)
    #   "2" if it encounters an error
    def execute_func(self):
        instr = self.get_code()

        if (instr[0] == 'D'):
            self.tape[self.position] = '1'
        if (instr[0] == 'X'):
            self.tape[self.position] = 'X'
        if (instr[0] == 'E'):
            self.tape[self.position] = ' '
        if (instr[0] == 'R'):
            self.position -= 1
        if (instr[0] == 'L'):
            self.position += 1
        if (instr[0] == '!'):
            return 1
        if (instr[0] == '?'):
            return 2

        self.dial = instr[1]
        # check position is valid
        if(self.position < 0 or self.position > len(self.tape)):
            print("Error: head went out of bounds")
            return 2 # error
        return 0

    # prints the current state of the machine
    def print_state(self):
        output = ''.join(self.tape)
        code = str(self.get_code()[0]) + str(self.get_code()[1]) 

        for i in range(len(output)):
            if i == self.position:
                print(f'| {output[i]}({self.dial})', end='')
            else:
                print(f'| {output[i]}   ', end='')

        print(f"| {code}")
        return
    
# main loop
def main():
    while(True):
        print("-=-=-=-=-=-=-=-=-=-=-=-=-\n")
        print("Input Turing Machine Tape Below:")
        print("(Or type 'help' for an example input.)")
        turing_tape = input().upper()
        print() # new line

        if (turing_tape == 'HELP'):
            print("use {'X',' ' (whitespace), '1'} to represent the tape, and use (1), (2), ... (6) to the right of a symbol to represent where the head begins and with what initial dial position.")
            print("Example Input: ' X11X X1(1)X '")
            time.sleep(3)
            print()
            continue
        # ensure Turing tape is valid:
        if (not has_only_allowed_characters(turing_tape)):
            print("Please use only allowed characters. (X, whitespace, 1 and the following: (1), (2), ... (6) )\n")
            time.sleep(2)
            continue
        if (not has_only_one_head_input(turing_tape)):
            print("Please include exactly one Head/dial input. ('(1)', or '(2)' etc. )\n")
            print("Example Input: ' X11X X1(1)X '")
            time.sleep(2)
            continue

        # Turing Tape is valid
        (tape, head_pos, dial_pos) = parse_turing_tape(turing_tape)
        my_machine = machine(tape, head_pos, dial_pos)
        my_machine.main_loop(verbose = True)
        input("Press enter to continue")

# returns:
#   True iff the input tape only has one head/dial
def has_only_one_head_input(turing_tape):
    valid_substrings = {'(1)', '(2)', '(3)', '(4)', '(5)', '(6)'}

    # regular expressions for string matching.
    pattern = '|'.join(map(re.escape, valid_substrings))

    matches = re.findall(pattern, turing_tape)
    
    return len(matches) == 1 and turing_tape.count(matches[0]) == 1

# returns:
#   True iff the input tape only allowed characters
def has_only_allowed_characters(turing_tape):
    allowed_characters = {'1', '2', '3', '4', '5', '6', 'X', ' ', '(', ')'} # is sent to lower case
    for char in turing_tape:
        if char not in allowed_characters:
            return False
    return True

# returns: (tuple)
#   (string, int, int) -- (Turing Tape, head_position, dial_position)
def parse_turing_tape(turing_tape):
    valid_head_positions = {'(1)', '(2)', '(3)', '(4)', '(5)', '(6)'}
    
    match = -1
    for head_string in valid_head_positions:
        match = turing_tape.find(head_string)
        if match == -1:
            continue
        break

    dial_position = int(turing_tape[match + 1])
    head_position = match - 1 # to the left of the symbol
    tape = turing_tape[0:match] + turing_tape[match+3:] # removes head input
    return (tape, head_position, dial_position)

main()