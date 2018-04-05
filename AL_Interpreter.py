#AL Interpreter
#Python 3.6.4
import sys
import math
input_memory = []
label_table={}
symbol_table={}

#function to Check the syntax of the labels
def VerifySyntax_LBL(token):
    if token.isalnum() and token.isupper() and token[0].isalpha():
        return
    else:
        print('Error: Wrong Syntax {}. Check Documentation'.format(token))
        sys.exit()
#function to Check Operands syntax
def VerifySyntax_OPD(token):
    if( token.isalnum() and token.isupper() and token[0].isalpha()) or token.isnumeric() or (token[:1]=='-' and token[1:].isnumeric()):
        return
    else:
        print('Error: Wrong Syntax {}. Check Documentation'.format(token))
        sys.exit()

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

#function that returns value from either a numeric or a symbol
def symbol_or_variable(opn):
    if opn.isnumeric() or (opn[:1]=='-' and opn[1:].isnumeric()):
        return int(opn)
    else:
        if opn in symbol_table:
            return int(symbol_table[opn])
        else:
            print("{} was not defined".format(opn))

#function to format the lines by removing spaces
def clean_line(line):
    line  = ''.join(line.split())
    return str(line)

#function that takes a full operation then returns the tokens
def parse_operation(operation):
    op = str(operation[5:9]).rstrip()
    VerifySyntax_LBL(op)
    opn1 = str(operation[10:14]).rstrip()
    opn2 = str(operation[15:19]).rstrip()
    opn3 = str(operation[20:24]).rstrip()
    VerifySyntax_OPD(opn1)
    VerifySyntax_OPD(opn2)
    VerifySyntax_OPD(opn3)
    return op,opn1,opn2,opn3

#Instruction Set
def ADD(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    opn2 = symbol_or_variable(opn2)
    Sum = opn1 + opn2
    if abs(Sum) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        Sum = truncate(Sum)
    Sum = round(Sum)
    symbol_table[opn3] = Sum
    return program_counter,input_pointer

def SUB(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    opn2 = symbol_or_variable(opn2)
    sub = opn1 - opn2
    if abs(sub) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        sub = truncate(sub)
    sub = round(sub)
    symbol_table[opn3] = sub
    return program_counter,input_pointer

def READ(opn1,opn2,opn3,program_counter,input_pointer):
    if(input_pointer>=len(input_memory)):
        print("Error: No input left to read @{}".format(program_counter))
        sys.exit()
    elif(abs(int(input_memory[input_pointer]))>9999999999):
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        read_input = truncate(input_memory[input_pointer])
        symbol_table[opn3] = read_input
    else:
        symbol_table[opn3] = input_memory[input_pointer]
    input_pointer += 1
    return program_counter,input_pointer

def WRIT(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    print("Output: {}".format(opn1))
    return program_counter,input_pointer

def ASGN(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    symbol_table[opn3] = opn1
    return program_counter,input_pointer

def MULT(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    opn2 = symbol_or_variable(opn2)
    print("{}  {}".format(opn1,opn2))
    mult = opn1 * opn2
    if abs(mult) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        mult = truncate(mult)
    mult = round(mult)
    symbol_table[opn3] = mult
    return program_counter,input_pointer

def DIV(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    opn2 = symbol_or_variable(opn2)
    div = opn1/opn2
    if abs(div) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        div = truncate(div)
    div = round(div)
    symbol_table[opn3] = div
    return program_counter,input_pointer

def SQR(opn1,opn2,opn3,program_counter,input_pointer):
    sqr = symbol_or_variable(opn1)**2
    if abs(sqr) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        sqr = truncate(sqr)
    sqr = round(sqr)
    symbol_table[opn3] = sqr
    return program_counter,input_pointer

def SQRT(opn1,opn2,opn3,program_counter,input_pointer):
    Sqrt = math.sqrt(symbol_or_variable(opn1))
    if abs(Sqrt) > 9999999999:
        print("Data Overflow/Underflow @ {}, result will be truncated...".format(program_counter))
        Sqrt = truncate(Sqrt)
    Sqrt = round(Sqrt)
    symbol_table[opn3] = Sqrt
    return program_counter,input_pointer


def EQL(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    opn2 = symbol_or_variable(opn2)
    if(opn1==opn2):
        program_counter = label_table[opn3]
    else:
        program_counter +=1
    return program_counter,input_pointer

def NEQ(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    opn2 = symbol_or_variable(opn2)
    if(opn1!=opn2):
        program_counter = label_table[opn3]
    else:
        program_counter +=1
    return program_counter,input_pointer

def GTEQ(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    opn2 = symbol_or_variable(opn2)
    if(opn1>=opn2):
        program_counter = label_table[opn3]
    else:
        program_counter +=1
    return program_counter,input_pointer

def LT(opn1,opn2,opn3,program_counter,input_pointer):
    opn1 = symbol_or_variable(opn1)
    opn2 = symbol_or_variable(opn2)
    if(opn1<opn2):
        program_counter = label_table[opn3]
    else:
        program_counter +=1
    return program_counter,input_pointer

def ITJP(opn1,opn2,opn3,program_counter,input_pointer):
    #handles symbols only when it comes to the index because
    #updating a constant doesn't sound useful at all(infinite loop?)
    symbol_table[opn1] += 1
    opn1 = symbol_table[opn1]
    opn2 = symbol_or_variable(opn2)
    if(opn1<opn2):
        program_counter = label_table[opn3]
    else:
        program_counter +=1
    return program_counter,input_pointer


def STOP(opn1,opn2,opn3,program_counter,input_pointer):
    sys.exit()


def RDAR(opn1,opn2,opn3,program_counter,input_pointer):
    opn2 = symbol_or_variable(opn2)
    symbol_table[opn3] = symbol_table[opn1][opn2]
    return program_counter,input_pointer



def WTAR(opn1,opn2,opn3,program_counter,input_pointer):
    opn3 = symbol_or_variable(opn3)
    symbol_table[opn2][opn3]=symbol_table[opn1]
    return program_counter,input_pointer



if __name__ == "__main__":
    sys.stdout = open('outputAL.txt', 'w')
    data_memory = []
    program_memory = []
    memory_dict = {0: data_memory, 1: program_memory, 2: input_memory}
    memory_status = 0
    counter = 0
    flag = 0
    data_declarated_size =0
    program_counter = 0
    input_pointer = 0
    operations_dict = {'ASGN': ASGN, 'ADD': ADD, 'SUB': SUB, 'MULT': MULT, 'DIV': DIV, 'SQR': SQR, 'SQRT': SQRT, 'EQL': EQL, 'NEQ': NEQ, 'GTEQ': GTEQ, 'LT': LT, 'RDAR':RDAR, 'WTAR':WTAR, 'ITJP':ITJP, 'READ':READ, 'WRIT':WRIT, 'STOP':STOP}

    with open('ALfiles/AL1.txt') as f:
        for line in f:
            counter += 1
            #the next 2 lines handle comments
            if(line.lstrip()[:1]=='*' or len(line.strip()) == 0):
                continue
            if(counter < 1000):
                if (line[:4]!="INT " and flag == 0):
                    flag += 1
                    memory_status += 1
                    counter = 0
                elif(clean_line(line).isnumeric() and flag == 1):
                    flag +=1
                    memory_status += 1
                    counter = 0
                memory_dict[memory_status].append(line.rstrip())
            else:
                sys.exit('You have not respected the machine\'s specifications')


    #Treating Data Declarations:
    #we will save the variables into an array to make their access and modification easy.
    #We assume that INT variables can be instanciated but Arrays can not
    for line in data_memory:
        data_declarated_size += int(line[10:14])
        if data_declarated_size<=1000:
            if int(line[10:14])==1:
                temp = 0
                if(line[15:26].rstrip()!=''):
                    temp = int(line[15:26].rstrip())
                symbol_table[str(line[5:9].rstrip())]=temp
            else:
                listofzeros = [0] * int(line[10:14])
                symbol_table[str(line[5:9].rstrip())]= list(listofzeros)
        else:
            print("Machine restrictions were not respected. {} variables declared".format(data_declarated_size))
            sys.exit()




    ##Looking for labels and adding them to the label table
    for line in program_memory:
        if line[0:4]!='    ':
            VerifySyntax_LBL(str(line[0:4]).rstrip())
            label_table[str(line[0:4]).rstrip()]=program_counter
        program_counter += 1


    #Here we get started with program_memory
    program_counter = 0
    while(True):
        if program_counter >= (len(program_memory)):
            break
        op, opn1, opn2, opn3 = parse_operation(program_memory[program_counter])
        if(op in operations_dict):
            program_counter,input_pointer = operations_dict[op](opn1,opn2,opn3,program_counter,input_pointer)
        else:
            print('operation doesn\'t exist @ {} {}'.format(program_counter, op))
            sys.exit()
        if(op in ['EQL', 'NEQ', 'GTEQ', 'LT', 'ITJP']): # in case of branching, continue so the program counter is not incremented
            continue
        program_counter += 1
