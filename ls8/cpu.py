"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0b0] * 0xFF
        self.reg = [0] * 8    #create 8 registers
        self.pc = 0           #program counter set to 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.push = 0b01000101
        self.pop = 0b01000110
        self.sp = self.reg[7]
        self.CALL = 0b01010000
        self.ADD = 0b10100000
        self.RET = 0b00010001

    def ram_read(self, value):
        return(self.ram[value])

    def ram_write(self, value, address):
        self.ram[address] = value


    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            print((instruction))
            self.ram[address] = instruction
            address += 1
        print('')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # set running variable
        
        running = True
        while running:
      
            #load the current command
            instruction = self.ram[self.pc]

            #check if it is the halt
            if instruction == self.HLT:
                running = False
                self.pc += 1
            
            elif instruction == self.LDI:
                #one RAM entries out determines which registrar is loaded
                reg_slot = self.ram_read(self.pc + 1)
                #two ram entries out determines what value is loaded
                int_value = self.ram_read(self.pc + 2)
                
                self.reg[reg_slot] = int_value
                #the program counter is set 3 entries ahead

                self.pc += 3

            elif instruction == self.PRN:
                 reg_slot = self.ram_read(self.pc + 1)
                 print(self.reg[reg_slot])
                 self.pc += 2

            elif instruction == self.MUL:
                reg_slot_1 = self.ram[self.pc+1]
                reg_slot_2 = self.ram[self.pc+2]
                self.alu('MUL',reg_slot_1,reg_slot_2)
                self.pc +=3

            elif instruction == self.ADD:
                slot1 = self.ram_read(self.pc + 1)
                slot2 = self.ram_read(self.pc + 2)
                self.alu('ADD', slot1, slot2)
                self.pc += 3

            elif instruction == self.push:
                reg_slot = self.ram[self.pc+1]
                val = self.reg[reg_slot]
                
                self.sp -= 1
             
                self.ram[self.sp] = val
                self.pc += 2
            
            elif instruction == self.pop:
                reg_slot = self.ram[self.pc+1]      
               
                value = self.ram[self.sp]
                self.reg[reg_slot] = value
                     
                self.sp += 1
                self.pc +=2

            elif instruction == self.CALL:
                return_address = self.pc + 2
                #decriment the stack pointer by 1
                self.sp -= 1
                #assign the new top of the stack the value of the return address
                self.ram[self.sp] = return_address

                #with the return addres stored
                #determine what registar slot is used for the called function
                reg_slot = self.ram[self.pc+1]
                #the subroutine location is the value at that designated reg slot
                subroutine_location = self.reg[reg_slot]
                #the program counter is set to the location of that sub routine
                self.pc = subroutine_location

            elif instruction == 0b00010001:
                return_address = self.ram[self.sp]
                self.sp += 1

                self.pc = return_address
            else:        
                print("I do not recognize that command")
                print(f"You are currently at Program Counter value: {self.pc}")
                print(f"The command issued was: {self.ram_read(self.pc)}")
                sys.exit(1)