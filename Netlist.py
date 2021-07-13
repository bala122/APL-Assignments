from sys import argv, exit

"""
It's recommended to use constant variables than hard-coding them everywhere.
For example, if you decide to change the command from '.circuit' to '.start' later,
    you only need to change the constant
"""
CIRCUIT = '.circuit'
END = '.end'


if len(argv) != 2:   #if arguments accepted via terminal are not enough it prints the same
    print('\nThe number of arguments are not enough')
    exit()

"""
The use might input a wrong file name by mistake.
In this case, the open function will throw an IOError.
Make sure you have taken care of it using try-catch
"""
try:
    with open(argv[1]) as f:
        lines = f.readlines()
        start = -1; end = -2
        for line in lines:              # extracting circuit definition start and end lines
            if CIRCUIT == line[:len(CIRCUIT)]:
                start = lines.index(line) #defining the start index
            elif END == line[:len(END)]:
                end = lines.index(line)   #defining the end index
                break
        if start >= end:                # validating circuit block
            print('Invalid circuit definition')
            exit(0)
        
        lis = []    
        for line in lines[start+1:end] :
        	lis.append(' '.join(reversed(line.split('#')[0].split()))) # appending reversed words and reversed lines in a reversed order in a list.
        
        
        lis = reversed(lis)                 # print output
              
        for l in lis:
            print(l)
        f.close()
except IOError:
    print('Invalid file')
    exit()



