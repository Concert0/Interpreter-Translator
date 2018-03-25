#PCL Interpreter
#Python 3.6.4
#This program does not handle floating point operations
import sys
import math
input_memory = []
def clean_line(line):
    line  = ''.join(line.split())
    return int(line)

def truncate(variable):
    ## In this function we only keep track of the 10 right digits
    ## 9999999999 + 1 would lead to 10000000000 which is a 0
    ## This won't be handled as the user should not enter such values
    ## So an overflow won't lead to an error but a wrong output
    trunc = 1
    if variable < 0:
        trunc = -1
    variable = trunc*(abs(variable)%(10**10))
    return variable

def parse_operation(operation):
    op = math.floor(abs(operation)/(10**9))
    if(operation<0):
        op *= -1
    opn1 = math.floor(abs(operation)/(10**6)) % (10**3)
    opn2 = math.floor(abs(operation)/(10**3)) % (10**3)
    opn3 = abs(operation) % (10**3)
    return op,opn1,opn2,opn3
##Operations tested
def ADD(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    Sum = data_memory[opn1] + data_memory[opn2]
    if abs(Sum) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        Sum = truncate(Sum)
    Sum = round(Sum)
    data_memory[opn3] = Sum
    return data_memory,program_counter,input_pointer

def ASGN(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    data_memory[opn3] = data_memory[opn1]
    return data_memory,program_counter,input_pointer

def READ(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    if(input_pointer>=len(input_memory)):
        print("Error: No input left to read @{}".format(program_counter))
        sys.exit()
    elif(abs(input_memory[input_pointer])>9999999999):
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        read_input = truncate(input_memory[input_pointer])
        data_memory[opn3] = read_input
    else:
        data_memory[opn3] = input_memory[input_pointer]
    input_pointer += 1
    return data_memory,program_counter,input_pointer

def WRIT(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    print("Output: {}".format(data_memory[opn1]))
    return data_memory,program_counter,input_pointer

def SUB(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    sub = data_memory[opn1] - data_memory[opn2]
    if abs(sub) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        sub = truncate(sub)
    sub = round(sub)
    data_memory[opn3] = sub
    return data_memory,program_counter,input_pointer

def MULT(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    mult = data_memory[opn1] * data_memory[opn2]
    if abs(mult) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        mult = truncate(mult)
    mult = round(mult)
    data_memory[opn3] = mult
    return data_memory,program_counter,input_pointer

def DIV(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    div = data_memory[opn1] / data_memory[opn2]
    if abs(div) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        div = truncate(div)
    div = round(div)
    data_memory[opn3] = div
    return data_memory,program_counter,input_pointer

def SQR(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    sqr = data_memory[opn1]**2
    if abs(sqr) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        sqr = truncate(sqr)
    sqr = round(sqr)
    data_memory[opn3] = sqr
    return data_memory,program_counter,input_pointer

def SQRT(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    Sqrt = math.sqrt(data_memory[opn1])
    if abs(Sqrt) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        Sqrt = truncate(Sqrt)
    Sqrt = round(Sqrt)
    data_memory[opn3] = Sqrt
    return data_memory,program_counter,input_pointer

def EQL(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    if(data_memory[opn1]==data_memory[opn2]):
        program_counter = opn3
    else:
        program_counter +=1
    return data_memory,program_counter,input_pointer

def NEQ(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    if(data_memory[opn1]!=data_memory[opn2]):
        program_counter = opn3
    else:
        program_counter +=1
    return data_memory,program_counter,input_pointer

def GTEQ(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    if(data_memory[opn1]>=data_memory[opn2]):
        program_counter = opn3
    else:
        program_counter +=1
    return data_memory,program_counter,input_pointer

def LT(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    if(data_memory[opn1]<data_memory[opn2]):
        program_counter = opn3
    else:
        program_counter +=1
    return data_memory,program_counter,input_pointer

def ITJP(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    data_memory[opn1] += 1
    if(data_memory[opn1]<data_memory[opn2]):
        program_counter = opn3
    else:
        program_counter +=1
    return data_memory,program_counter,input_pointer

def STOP(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    sys.exit()


def RDAR(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    data_memory[opn3] = data_memory[opn1+data_memory[opn2]]
    return data_memory,program_counter,input_pointer



def WTAR(data_memory,opn1,opn2,opn3,program_counter,input_pointer):
    data_memory[opn2+data_memory[opn3]] = data_memory[opn1]
    return data_memory,program_counter,input_pointer

##Operations being tested



if __name__ == "__main__":
    # sys.stdout = open('output.txt', 'w')
    data_memory = []
    program_memory = []
    memory_dict = {0: data_memory, 1: program_memory, 2: input_memory}
    memory_status = 0
    operations_dict = {0: ASGN, 1: ADD, -1: SUB, 2: MULT,-2: DIV, 3: SQR, -3: SQRT,4: EQL, -4: NEQ, 5: GTEQ, -5: LT, 6:RDAR, -6:WTAR, 7:ITJP, 8:READ, -8:WRIT, 9:STOP}
    counter = 0
    program_counter = 0
    input_pointer = 0
    with open('al2pcl.txt') as f:
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
    #fill the rest of data memory with 0s
    while(len(data_memory)<1000):
        data_memory.append(0)

    while(True):
        # print(data_memory)
        op, opn1, opn2, opn3 = parse_operation(program_memory[program_counter])
        # print("{}  {}  {}  {}".format(op, opn1, opn2, opn3))
        if(op in operations_dict):
            data_memory,program_counter,input_pointer = operations_dict[op](data_memory,opn1,opn2,opn3,program_counter,input_pointer)
        else:
            print('operation doesn\'t exist @ {} {}'.format(program_counter, op))
            sys.exit()
        if(op in [4,-4,5,-5,7]): # in case of branching, continue so the program counter is not incremented
            continue
        program_counter += 1
        if program_counter == len(program_memory):
            break
    # print(data_memory)


    # for x in data_memory:
    #     print(x)
    # print('#######')
    # for x in program_memory:
    #     print(x)
    # print('#######')
    # for x in input_memory:
    #     print(x)
