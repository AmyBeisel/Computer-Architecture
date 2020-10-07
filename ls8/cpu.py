"""CPU functionality."""

import sys

HLT = 0b00000001 #halt 
LDI = 0b10000010 
PRN = 0b01000111 #Print
MUL = 0b10100010 #Multiply
ADD = 0b10100000 #Addition
PUSH = 0b01000101 #push in stack
POP = 0b01000110 #pop in stack


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[7] = 0xF4
        self.pc = 0
        self.halted = False
    #Memory address
    def ram_read(self, address):
        return self.ram[address]
    #Memory data
    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""
        
        address = 0
        with open(filename) as fp:
            for line in fp:
                line_split = line.split("#")
                num = line_split[0].strip()
                if num == '':
                    continue
                value = int(num, 2)
                self.ram[address] = value
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
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
        
        while not self.halted:
            #Instruction Register. internal part of CPU that holds a value
            instruction_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc +1)
            operand_b = self.ram_read(self.pc +2)
            self.execute_instruction(instruction_to_execute, operand_a, operand_b)
    #helper function
    def execute_instruction(self, IR, operand_a, operand_b):
        if IR == HLT:
            self.halted = True
            self.pc += 1
        elif IR == LDI:
            self.reg[operand_a] = operand_b
            self.pc +=3
        elif IR == PRN:
            print(self.reg[operand_a])
            self.pc += 2
        
        elif IR == ADD:
            self.alu("ADD", operand_a, operand_b)
            self.pc += 3
        elif IR == MUL:
            self.alu("MUL", operand_a, operand_b)
            self.pc += 3
        
        elif IR == PUSH:
            #decrement the stack pointer 
            self.reg[7] -=1
            #set R7 to variable SP
            SP = self.reg[7]
            #store the value in the register onto the top of the stack
            value = self.reg[operand_a]
            self.ram[SP] = value
            #increment pc
            self.pc +=2
        elif IR == POP:
            #read the value from the top of the stack
            SP = self.reg[7]
            #store the value to the given register
            value = self.ram[SP]
            self.reg[operand_a] = value
            #increment stack pointer
            self.reg[7] +=1
            self.pc +=2

        else:
            print("ehh idk what to do")
            sys.exit(1)
            
 
        

        


