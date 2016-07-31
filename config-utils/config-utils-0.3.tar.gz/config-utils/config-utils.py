
class ReadConfig(object):

    def __init__(self, file_name, *args):
        self.options_from_config = []
        self.variable = []
        self.value = []
        self.value_list = []

        for num in args:
            self.options_from_config.append(num)
        self.file_name = file_name

        # open file and read contents to store in variables
        with open(file_name) as f:
            content = f.readlines()
        line_num = 1
        for line in content:
            if not line.startswith('#') and not line.isspace():
                if not self.contains("=", line):
                    self.raiseGeneralError("Could not find an '=' %d: %s" %  (line_num, line))


                self.variable.append(line.split()[0])
                equal    = line.split()[1]
                self.value.append(line.split()[2])

                if len(line.split()) > 3:
                    self.raiseGeneralError("Wrong Syntax on line, %s: %s" % (line_num, line))
                if equal != '=':
                    raise StandardError("Could not find '=' on line %s : %s" % (line_num, line))


            line_num += 1
        for val in self.variable:
            if val not in self.options_from_config:
                raise StandardError("Could not find '%s' in config file" % val)

        self.value_list = self.value

    def contains(self, character, string):
        equals = 0
        for char in string:
            if char == character:
                equals += 1
        if equals == 0:
            return False
        else:
            return True

    def raiseGeneralError(self, *args):
        exit(*args)

