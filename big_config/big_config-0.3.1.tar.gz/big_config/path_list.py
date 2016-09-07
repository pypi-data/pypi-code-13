import os

from big_config.constants import COMMENT_MARK


class PathAsList(list):
    """
        inherits from list and adds specific methods
        for a model defining a path with a list of dirs
    """

    def __init__(self, parent=""):
        super(PathAsList, self).__init__(self)
        if parent:
            self.append(parent)

    # go down one level
    def down(self, elem):
        self.append(elem)

    # go up n levels
    def up(self, levels=1):
        while levels < 0:
            del self[-1]
            levels += 1

    # convert list to path string
    def to_path(self):
        return os.path.join(*self) if len(self) else ""


class Step(list):
    """
        inherits from list and adds specific methods to describe
        a list of indent increment steps in a list of paths
    """

    def __init__(self):
        super(Step, self).__init__(self)
        self.append(0)

    # compare current vs last indent value
    def inspect(self, indent):
        if indent > self[-1]:
            self.append(indent)
            return 1
        elif indent == self[-1]:
            return 0
        else:
            back_steps = 0
            while indent < self[-1]:
                del self[-1]
                back_steps -= 1
            return back_steps


class PathsList(list):
    def __init__(self, raw, parent=""):
        super(PathsList, self).__init__(self)
        # set the parent
        self.__current = PathAsList(parent)
        if raw and len(raw):
            self.add(raw)

    @staticmethod
    def get_indent(line):
        return len(line) - len(line.lstrip())

    # clean and prepare raw list for processing
    @staticmethod
    def __prepare(raw):
        # declare an empty output
        output = []
        # declare a step instance
        step = Step()
        # strip comments and blank lines at the beginning
        while not raw[0].strip() or raw[0].strip()[0] == COMMENT_MARK:
            del raw[0]
        # detect a general indent
        ind0 = PathsList.get_indent(raw[0])

        for elem in raw:
            # if blank or comment ignore
            if not elem.strip() or elem.strip()[0] == COMMENT_MARK:
                continue
            # get the current line's indent
            ind = PathsList.get_indent(elem) - ind0
            # append to output a tuple containing the step and the clean string
            output.append((step.inspect(ind), elem.strip()))
        return output

    def __add_elem(self, elem, last):
        # if step goes deeper add the last element to the current path list
        if elem[0] == 1:
            self.__current.down(last)
        # if step goes up add the last element to the current path list
        if elem[0] < 0:
            self.__current.up(elem[0])
        # append the resulting path
        self.append(os.path.join(self.__current.to_path(), elem[1]))

    def add(self, raw):
        data = self.__prepare(raw)
        # keep the last element
        last = None
        for elem in data:
            self.__add_elem(elem, last)
            # update the last element
            last = elem[1]
