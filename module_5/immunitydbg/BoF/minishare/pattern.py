#!/usr/bin/python

import sys
import argparse

program_description = 'Inputs a string to find the offset in the constant alphanumeric string'
parser = argparse.ArgumentParser(program_description)
parser.add_argument("pattern", nargs="?", help="a pattern to be anazlyed for the offset in constant alphanumeric string")
args = parser.parse_args()

input_pattern = ''

if args.pattern:                    # when input is from user 
    input_pattern = args.pattern
    print 'hello world from user input', input_pattern
elif not sys.stdin.isatty():        # when standard input is from terminal
    input_pattern = sys.stdin.read()
    print 'hello world from terminal input', input_pattern
else:                               # when there is no input
    parser.print_help()

def main(pattern):
    print "pattern we are matching", pattern
    # set up our string 
    upper_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_alpha = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    
    # NOTE: this is the same string pattern as the generated string by unique.py
    try:
        string = ''
        for i in range(len(upper_alpha)):
            for j in range(len(lower_alpha)):
                for k in range(len(digits)):
                    string = string + upper_alpha[i] + lower_alpha[j] + digits[k]
 
        offset = string.find(pattern)
    except:
        print 'string building didnt work' 

    print offset


if __name__ == '__main__':
    main(input_pattern)
    sys.exit(0)
