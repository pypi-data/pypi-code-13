# SMOP compiler -- Simple Matlab/Octave to Python compiler
# Copyright 2011-2016 Victor Leikehman

import sys
import lexer
import options

def main():
    new_lexer = lexer.new()
    line = ""
    while 1:
        try:
            line += (raw_input("=>> ")+"\n").decode("string_escape")
            print len(line), [c for c  in line]
        except EOFError:
            try:
                new_lexer.input(line)
                for tok in new_lexer:
                    print tok 
                line = ""
            except Exception as ex:
                print ex
        except KeyboardInterrupt:
            break
        except Exception as ex:
            print ex
            continue

if __name__ == "__main__":
    options.do_testing = 1
    main()
    # lexer = new()
    # buf = open(sys.argv[1]).read()
    # lexer.input(buf)
    # for tok in lexer:
    #     print tok

