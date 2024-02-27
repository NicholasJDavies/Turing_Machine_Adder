# Author: Nicholas Davies

MAX_LOOPS = 1000

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
    def __init__(self,  tape, position, dial):
        arr = [char for char in tape]
        self.tape = [' ' for i in range(5)] + arr + [' ' for i in range(5)]
        self.position = position + 5
        self.dial = dial

    def main_loop(self, verbose=True):
        output = 0
        loops = 0
        while(output == 0 and loops < MAX_LOOPS):
            if(verbose):
                self.print_state()
            output = self.execute_func()
            loops += 1

        self.print_state()

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


    def get_code(self):
        code = self.tape[self.position]
        instr = machine.instructions[code, self.dial]
        return instr
        
    # executes function on tape
    # returns "1" when done, 
    # "0" if continuing, 
    # "2" if it encounters an error
    def execute_func(self):
        instr = self.get_code()

        match (instr[0]):
            case 'D':
                self.tape[self.position] = '1'
            case 'X':
                self.tape[self.position] = 'X'
            case 'E':
                self.tape[self.position] = ' '
            case 'R':
                self.position -= 1
            case 'L':
                self.position += 1
            case '!':
                return 1
            case '?':
                return 2

        self.dial = instr[1]
        return 0

    # prints the state of the machine
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
    my_machine = machine(" X111X X1X ", 7, 1)
    my_machine.main_loop(verbose = True)

main()
print("\n\n")