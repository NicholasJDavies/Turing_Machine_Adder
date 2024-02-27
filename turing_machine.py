# Author: Nicholas Davies

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
    '''

    def __init__(self,  tape, position, dial):
        arr = [char for char in tape]
        self.tape = [' ' for i in range(5)] + arr + [' ' for i in range(5)]
        self.position = position + 5
        self.dial = dial

    # executes function on tape
    # returns "1" when done, 
    # "0" if continuing, 
    # "2" if it encounters an error
    def execute_func(self):
        code = self.tape[self.position]

        match (code, self.dial):

            case (' ', 1):
                self.tape[self.position] = '1'
                self.dial = 6
            case (' ', 2):
                self.position -= 1
                self.dial = 2
            case (' ', 3):
                self.position -= 1
                self.dial = 3
            case (' ', 4):
                self.position += 1
                self.dial = 4
            case (' ', 5):
                self.position += 1
                self.dial = 5
            case (' ', 6):
                self.tape[self.position] = 'X'
                self.dial = 6

            case ('X', 1):
                self.tape[self.position] = ' '
                self.dial = 2
            case ('X', 2):
                self.tape[self.position] = ' '
                self.dial = 3    
            case ('X', 3):
                self.tape[self.position] = ' '
                self.dial = 4
            case ('X', 4):
                return 2 # error
            case ('X', 5):
                return 2 # error
            case ('X', 6):
                return 1 # Halt

            case ('1', 1):
                self.position -= 1
                self.dial = 1
            case ('1', 2):
                return 2 # error
            case ('1', 3):
                self.tape[self.position] = ' '
                self.dial = 5
            case ('1', 4):
                self.position -= 1
                self.dial = 6
            case ('1', 5):
                self.position -= 1
                self.dial = 1
            case ('1', 6):
                self.position -= 1
                self.dial = 3

        return 0

    # prints the state of the machine\
    def print_state(self):
        # output = ' ' +  self.tape.lstrip().rstrip() + ' '
        output = ''.join(self.tape)

        for i in range(len(output)):
            if i == self.position:
                print(f'| {output[i]}({self.dial})', end='')
            else:
                print(f'| {output[i]}   ', end='')

        print("|")
        return
    
# main loop
def main():
    my_machine = machine(" X1X X1X ", 6, 1)
    my_machine.print_state()
    output = 0
    MAX_LOOPS = 100000
    loops = 0
    while(output == 0 and loops < MAX_LOOPS):
        output = my_machine.execute_func()
        my_machine.print_state()
        loops += 1

    print()
    print()

main()