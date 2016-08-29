class Infdent():
    def __init__(self,spaces=4,indent=False):
        self.tab = "".join([" " for x in range(spaces)])
        self.tabs = 0
        self.indent = indent

    @property
    def gettabs(self):
        return "".join([self.tab for x in range(self.tabs)])

    def __call__(self,*strings,end="\n",indent=None):
        if indent is None:
            indent = self.indent
        for string in strings:
            if string is None:
                self.rset
                continue
            if "\n" in string:
                string = string.split("\n")

            if isinstance(string,list):
                for line in string:
                    print(self.gettabs + line,end=end)
                    if indent:
                        self.tabs += 1
            elif isinstance(string,tuple):
                for line in string:
                    print(self.gettabs + line,end=end)
                    if indent:
                        self.tabs += 1
            elif isinstance(string,str):
                print(self.gettabs + string,end=end)
                if indent:
                    self.tabs += 1
            else:
                print(self.gettabs + string,end=end)
                if indent:
                    self.tabs += 1
        if not indent:
            self.tabs += 1

    @property
    def rset(self):
        self.tabs = 0

    def set(self,tabs):
        self.tabs = tabs

if __name__ == "__main__":
    tabs = Infdent()

    tabs("Hello","Hello",None)
    tabs("Hello","Hello")

    tabs.rset
    tabs(["Hey","Hi","Hello"],indent=True)
    tabs(("Hey","Hi","Hello"))

    tabs.rset
    tabs("Hello\nHey")