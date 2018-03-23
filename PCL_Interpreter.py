#PCL Interpreter
#Python 3.6.4
import sys
import math
input_memory = []
def clean_line(line):
    line  = ''.join(line.split())
    return int(line)

def truncate(variable):
    variable %= (10**10)
    return variable

def parse_operation(operation):
    op = math.floor(abs(operation)/(10**9))
    if(operation<0):
        op *= -1
    opn1 = abs(math.floor(operation/(10**6))) % (10**3)
    opn2 = abs(math.floor(operation/(10**3))) % (10**3)
    opn3 = abs(operation % (10**3))
    return op,opn1,opn2,opn3

def ADD(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    # print("ADD")
    Sum = data_memory[opn1] + data_memory[opn2]
    if abs(Sum) > 999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated".format(program_counter))
        Sum = truncate(Sum)
    data_memory[opn3] = Sum
    return data_memory,program_counter,input_pointer

def ASGN(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    # print("ASGN")
    data_memory[opn3] = data_memory[opn1]
    return data_memory,program_counter,input_pointer

def READ(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    # print("READ")
    if(input_pointer>=len(input_memory)):
        print("No input left to read")
    elif(abs(input_memory[input_pointer])>9999999999):
        print("Data Overflow/Underflow @ {}, result will be truncated".format(program_counter))
        read_input = truncate(input_memory[input_pointer])
        data_memory[opn3] = read_input
        input_pointer += 1
    else:
        data_memory[opn3] = input_memory[input_pointer]
        input_pointer += 1
    return data_memory,program_counter,input_pointer

def WRIT(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    # print("WRIT")
    print("Output: {}".format(data_memory[opn1]))
    return data_memory,program_counter,input_pointer





if __name__ == "__main__":
    sys.stdout = open('output.txt', 'w')
    data_memory = []
    program_memory = []
    memory_dict = {0: data_memory, 1: program_memory, 2: input_memory}
    memory_status = 0
    # operations_dict = {0: ASGN, 1: ADD, -1: SUB, 2: MULT, -2: DIV, 3: SQR, -3: SQRT, 4: EQL, -4: NEQ, 5: GTEQ, -5: LT, 6:RDAR, -6:WTAR, 7:ITJP, -7:label, 8:READ, -8:WRIT, 9:STOP}
    operations_dict = {0: ASGN, 1: ADD, 8:READ, -8:WRIT}
    counter = 0
    program_counter = 0
    input_pointer = 0
    with open('test1.txt') as f:
        for line in f:
            counter += 1
            int_line = clean_line(line)
            if(counter < 1000):
                if int_line==+9999999999:
                    memory_status += 1
                    counter = 0
                    continue
                memory_dict[memory_status].append(int_line)
            else:
                sys.exit('You have not respected the machine\'s specifications')


    for operation in program_memory:
        program_counter += 1
        op, opn1, opn2, opn3 = parse_operation(operation)
        if(op in operations_dict):
            data_memory,program_counter,input_pointer = operations_dict[op](data_memory,opn1,opn2,opn3,program_counter,input_pointer)
        else:
            print('operation doesn\'t exist @ {} {}'.format(program_counter, op))


    # for x in data_memory:
    #     print(x)
    # print('#######')
    # for x in program_memory:
    #     print(x)
    # print('#######')
    # for x in input_memory:
    #     print(x)
