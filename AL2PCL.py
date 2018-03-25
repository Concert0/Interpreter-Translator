#AL to PCL
#Python 3.6.4
import sys
input_memory=[]
symbol_table={}
label_table = {}

def clean_line(line):
    line  = ''.join(line.split())
    return str(line)

def parse_operation(operation):
    op = str(operation[5:9]).rstrip()
    opn1 = str(operation[10:14]).rstrip()
    opn2 = str(operation[15:19]).rstrip()
    opn3 = str(operation[20:24]).rstrip()
    return op,opn1,opn2,opn3

def symbol_or_variable(opn):
    if opn.isnumeric():
        return "{0:0>3}".format(int(opn))
    else:
        if opn in symbol_table:
            return symbol_table[opn]
        else:
            print("{} was not defined".format(opn))

if __name__ == "__main__":
    sys.stdout = open('al2pcl.txt', 'w')
    data_memory = []
    program_memory = []
    memory_dict = {0: data_memory, 1: program_memory, 2: input_memory}
    memory_status = 0
    counter = 0
    flag = 0
    data_declarated_size =0
    program_counter = 0
    input_pointer = 0
    with open('test2A.txt') as f:
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
    PCL_PROGRAM_MEMORY = []
    counter = 0
    for line in data_memory:
        if int(line[10:14])==1:
            symbol_table[str(line[5:9].rstrip())]= "{0:0>3}".format(counter)
            counter += 1
            print('+0 000 000 000')
        else:
            symbol_table[str(line[5:9].rstrip())]= "{0:0>3}".format(counter)
            for i in range(int(line[10:14])):
                print('+0 000 000 000')

        if data_declarated_size>1000:
            print("Machine restrictions were not respected. {} variables declared".format(data_declarated_size))
            sys.exit()
        data_declarated_size += int(line[10:14])
    # print(symbol_table)
    print("+9 999 999 999")


    ##Looking for labels and adding them to the label table
    for line in program_memory:
        if line[0:4]!='    ':
            label_table[str(line[0:4]).rstrip()]="{0:0>3}".format(program_counter)
        program_counter += 1
    # print(label_table)





    operations_dict = {'ASGN': '+0', 'ADD': '+1', 'SUB': '-1', 'MULT': '+2', 'DIV': '-2', 'SQR': '+3', 'SQRT': '-3', 'EQL': '+4', 'NEQ': '-4', 'GTEQ': '+5', 'LT': '-5', 'RDAR':'+6', 'WTAR':'-6', 'ITJP':'+7', 'READ':'+8', 'WRIT':'-8', 'STOP':'+9'}



    #Here we get started with program_memory
    program_counter = 0
    while(True):
        if program_counter >= (len(program_memory)):
            break
        op, opn1, opn2, opn3 = parse_operation(program_memory[program_counter])
        if(op in ['ASGN', 'ADD', 'SUB', 'MULT', 'DIV', 'SQR', 'SQRT','RDAR', 'WTAR', 'READ', 'WRIT', 'STOP']):
            pcl_command = operations_dict[op] + ' ' + symbol_or_variable(opn1) +  ' ' + symbol_or_variable(opn2) + ' ' + symbol_or_variable(opn3)
            print(pcl_command)
        elif(op in ['EQL', 'NEQ', 'GTEQ', 'LT','ITJP']):
            if(opn3 in label_table):
                pcl_command = operations_dict[op] + ' ' + symbol_or_variable(opn1) +' ' + symbol_or_variable(opn2) + ' ' + label_table[opn3]
                print(pcl_command)
            else:
                print("Error: Label not found")
                sys.exit()
        else:
            print('operation doesn\'t exist @ {} {}'.format(program_counter, op))
            sys.exit()
        program_counter += 1

    print("+9 999 999 999")
    for i in input_memory:
        print(i)
