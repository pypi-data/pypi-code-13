import math

def prettymatrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = "\t".join("{{:{}}},".format(x) for x in lens)
    table = ["    "+fmt.format(*row) for row in s]
    return "\n".join(table)[:-1]

class Matrix():
    def __init__(self,array):
        self.array = array
        self.size = [len(array),len(array[0])]

        self.pre_repr = "Matrix({})".format(", ".join(["{}={}".format(num,row) for num,row in enumerate(self.array)]))
        self.pre_str = "Matrix([\n"+prettymatrix(self.array)+"\n])"
        self.flat = [item for sublist in self.array for item in sublist]

    def __getitem__(self,index):
        return self.flat[index]

    def __str__(self):
        return self.pre_str

    def __repr__(self):
        return self.pre_repr

    def __neg__(self):
        return self.scalar(op="--")

    def __pos__(self):
        return self.scalar(op="++")

    def __abs__(self):
        return self.scalar(op="abs")

    def __round__(self,operand=0):
        return self.scalar(operand,"rnd")

    def __ceil__(self):
        return self.scalar(op="cel")

    def __floor__(self):
        return self.scalar(op="flr")

    def __trunc__(self):
        return self.scalar(op="trc")

    def __sub__(self,operand):
        return self.result(operand,"-")

    def __pow__(self,operand):
        return self.result(operand,"**")

    def __add__(self,operand):
        return self.result(operand,"+")

    def __mul__(self,operand):
        return self.result(operand,"*")

    def result(self,operand,op="+"):
        if isinstance(operand,int):
            return self.scalar(operand,op)
        else:
            new_matrix = []
            operand = operand.rotate_right()
            for num,row in enumerate(self.array):
                new_row = []
                for a,b in zip(self.array[num],operand.array[num]):
                    if op == "+":
                        new_row.append(a+b)
                    elif op == "-":
                        new_row.append(a-b)
                    elif op == "*":
                        new_row.append(a*b)
                    elif op == "**":
                        new_row.append(a**b)
                new_matrix.append(new_row)

            return Matrix(new_matrix)

    def scalar(self,num=0,op="+"):
        new_matrix = []

        for row in self.array:
            new_column = []
            for column in row:
                if op == "+":
                    new_column.append(column+num)
                elif op == "-":
                    new_column.append(column-num)
                elif op == "*":
                    new_column.append(column*num)
                elif op == "**":
                    new_column.append(column**num)
                elif op == "--":
                    new_column.append(-column)
                elif op == "++":
                    new_column.append(+column)
                elif op == "abs":
                    new_column.append(abs(column))
                elif op == "rnd":
                    new_column.append(round(column,num))
                elif op == "flr":
                    new_column.append(math.floor(column))
                elif op == "cel":
                    new_column.append(math.ceil(column))
                elif op == "trc":
                    new_column.append(math.trunc(column))
            new_matrix.append(new_column)

        return Matrix(new_matrix)

    def flip(self):
        return Matrix(list(reversed(self.array)))

    def mirror(self):
        return Matrix([list(reversed(x)) for x in self.array])

    def rotate_right(self):
        return Matrix(list(zip(*list(reversed(self.array)))))

    def rotate_left(self):
        return Matrix(list(reversed(list(zip(*self.array)))))

if __name__ == "__main__":
    a = [
        [2, 2, 2],
        [2, 5, 2],
        [2, 2, 2]
    ]

    b = [
        [2, 2, 2],
        [2, 5, 2],
        [2, 2, 2]
    ]

    a = Matrix(a)
    b = Matrix(b)

    print(a+b)
    print(a-b)
    print(a*b)
    print(a**b)
    print(-a)
    print(+a)
    print(abs(a))
    print(round(a))
    print(math.floor(a))
    print(math.ceil(a))
    print(math.trunc(a))