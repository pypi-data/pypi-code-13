import sys,re
import optparse

MSG_USAGE = "usage: ppt [-d] [string ...] "


class Ppt:
    def __init__(self):
        self.options = self.parse_option()
        sys.stdout.write('___________\n')
        self.ppt()
        sys.stdout.write('___________\n')

    def parse_option(self):
        opt = optparse.OptionParser(MSG_USAGE)
        opt.add_option('-d',action = 'store_true' , metavar='[_00__.__0] -> a', help='reverse from holes to ASCII char')
        options, arguments = opt.parse_args()
        return options

    def ppt(self):
        if self.options.d:
            self.getppt()
        elif len(sys.argv[0:])==1:
            while 1:
                try:
                    line = sys.stdin.readline()
                except KeyboardInterrupt:
                    break
                if not line:
                    exit()
                for c in line:
                    self.putppt(c)

        else:
            i = 0
            for argc in sys.argv[1:]:
                if i > 0:
                    self.putppt(' ')
                for c in argc:
                    self.putppt(c)
                i += 1

    def putppt(self,c):
        sys.stdout.write('|')
        for i in range(7,-1,-1):
            if i == 2:
                sys.stdout.write('.')
            if ord(c)&(1<<i) :
                sys.stdout.write('o')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('|\n')

    def getppt(self):
        while 1:
            try:
                line = sys.stdin.readline()
            except KeyboardInterrupt:
                break
            if not line:
                exit()

            if len(line) != 10:
                sys.stderr.write('invalid input format ')
                exit()

            c = 0
            index = line.find('.')
            if index != -1:
                line = line.replace('.','')

            for i in range(0,8,1):
                if line[i] == 'o':
                    c = c | (1<<(7-i))
                # print i
            print  chr(c)

if __name__ == '__main__':
    ppt = Ppt()
    sys.stdout.write('___________\n')
    ppt.ppt()
    sys.stdout.write('___________\n')
