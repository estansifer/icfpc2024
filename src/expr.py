base94 = ''.join([chr(x) for x in range(33, 127)])
str_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`|~ \n'

N94 = 94
assert len(base94) == N94
assert len(str_chars) == N94

indicator2args = {
        'T' : 0,
        'F' : 0,
        'I' : 0,
        'S' : 0,
        'v' : 0,
        'U' : 1,
        'L' : 1,
        'B' : 2,
        '?' : 3
    }

def int_div(x, y):
    if x * y >= 0:
        return x // y
    if x < 0:
        return ((x - 1) // y) + 1
    else:
        return ((-x - 1) // (-y)) + 1

def int_mod(x, y):
    return x - y * int_div(x, y)

binaryops = {
        '+' : (int, int, lambda x, y : x + y),
        '-' : (int, int, lambda x, y : x - y),
        '*' : (int, int, lambda x, y : x * y),
        '/' : (int, int, int_div),
        '%' : (int, int, int_mod),
        '<' : (int, int, lambda x, y : x < y),
        '>' : (int, int, lambda x, y : x > y),
        '=' : (None, None, lambda x, y : x == y),
        '|' : (bool, bool, lambda x, y : x or y),
        '&' : (bool, bool, lambda x, y : x and y),
        '.' : (str, str, lambda x, y : x + y),
        'T' : (int, str, lambda x, y : y[:x]),
        'D' : (int, str, lambda x, y : y[x:]),
        }

class TreeExpr:
    def __init__(self, token, args):
        self.token = token
        self.indicator = token[0]
        self.name = token[1:]
        self.args = args

    # static
    def from_token_string(token_string):
        return TreeExpr.from_token_list(token_string.split())

    # static
    def from_token_list(tokens):
        stack = []
        for token in reversed(tokens):
            k = indicator2args[token[0]]
            assert len(stack) >= k
            cur = TreeExpr(token, stack[-1:-k-1:-1])
            if k > 0:
                stack = stack[:-k]
            stack.append(cur)
        assert len(stack) == 1
        return stack[0]

    def substitute(self, var_name, var_value):
        if self.indicator == 'L':
            if self.name == var_name:
                return self
        if self.indicator == 'v':
            if self.name == var_name:
                return var_value
        sub_args = [arg.substitute(var_name, var_value) for arg in self.args]
        return TreeExpr(self.token, sub_args)

    def to_token_list(self, accum = None):
        if accum is None:
            accum = []
        accum.append(self.token)
        for arg in self.args:
            arg.to_token_list(accum)
        return accum

    def to_token_string(self):
        return ' '.join(self.to_token_list())

    def all_variables(self, vs = None):
        if vs is None:
            vs = set()
        if self.indicator == 'v':
            vs.add(self.name)
        for arg in self.args:
            arg.all_variables(vs)
        return vs

    def __str__(self):
        if len(self.args) == 0:
            return self.token
        else:
            return self.token + '(' + ', '.join([str(arg) for arg in self.args]) + ')'

    def pretty_print(self):
        p = [a.pretty_print() for a in self.args]
        if self.indicator == 'I':
            return decode_integer(self.name)
        elif self.indicator == 'S':
            return '«' + decode_string(self.name) + '»'
        elif self.indicator in 'TF':
            return self.indicator
        elif self.indicator == 'L':
            return 'λ' + self.name + ': ' + p[0]
        elif self.indicator == 'v':
            return self.token
        elif self.indicator == 'U':
            return self.name + ' ' + p[0]
        elif self.indicator == 'B':
            return f'({p[0]}) {self.name} ({p[1]})'
        elif self.indicator == '?':
            return f'({p[0]}) ? ({p[1]}) : ({p[2]})'
        else:
            assert False

def decode_integer(name):
    value = 0
    for c in name:
        value *= N94
        value += ord(c) - 33
    return value

def decode_string(name):
    return ''.join([str_chars[ord(c) - 33] for c in name])

def encode_integer(i):
    result = []
    if i == 0:
        result.append(base94[0])
    while i > 0:
        result.append(base94[i % N94])
        i = (i // N94)
    return 'I' + ''.join(reversed(result))

def encode_string(s):
    result = []
    for c in s:
        idx = str_chars.find(c)
        assert idx >= 0
        result.append(base94[idx])
    return 'S' + ''.join(result)

def str2int(s):
    value = 0
    for c in s:
        idx = str_chars.find(c)
        assert idx >= 0
        value *= N94
        value += idx
    return value

def int2str(i):
    result = []
    while i > 0:
        result.append(str_chars[i % N94])
        i = (i // N94)
    return ''.join(reversed(result))

def eval_expr(expr, desired_type = None):
    result = None
    while result is None:
        t = expr.token
        i = expr.indicator
        name = expr.name
        args = expr.args

        if t == 'B$':
            function = eval_expr(args[0])
            assert function.indicator == 'L'
            expr = function.args[0].substitute(function.name, args[1])
        elif t == '?':
            if eval_expr(args[0], bool):
                expr = args[1]
            else:
                expr = args[2]
        elif i in ['L', 'v']:
            result = expr
        elif i in ['T', 'F', 'I', 'S']:
            if i == 'T':
                result = True
            if i == 'F':
                result = False
            if i == 'I':
                result = decode_integer(name)
            if i == 'S':
                result = decode_string(name)
        elif t == 'U-':
            result = -eval_expr(args[0], int)
        elif t == 'U!':
            result = not eval_expr(args[0], bool)
        elif t == 'U#':
            result = str2int(eval_expr(args[0], str))
        elif t == 'U$':
            result = int2str(eval_expr(args[0], int))
        elif i == 'B':
            op = binaryops[name]
            arg0 = eval_expr(args[0], op[0])

            # shortcut boolean operations
            if (name == '|') and arg0:
                arg1 = True
            elif (name == '&') and (not arg0):
                arg1 = False
            else:
                arg1 = eval_expr(args[1], op[1])

            result = op[2](arg0, arg1)
        else:
            assert False

    assert desired_type in [None, type(result)]
    return result

tests = [
        ('I-', 12),
        ("U- I$", -3),
        ("U! T", False),
        ("U# S4%34", 15818151),
        ("U$ I4%34", "test"),
        ("B+ I# I$", 5),
        ("B- I$ I#", 1),
        ("B* I$ I#", 6),
        ("B/ U- I( I#", -3),
        ("B% U- I( I#", -1),
        ("B< I$ I#", False),
        ("B> I$ I#", True),
        ("B= I$ I#", False),
        ("B| T F", True),
        ("B& T F", False),
        ("B. S4% S34", "test"),
        ("BT I$ S4%34", "tes"),
        ("BD I$ S4%34", "t"),
        ("? B> I# I$ S9%3 S./", "no"),
        ("B$ B$ L# L$ v# B. SB%,,/ S}Q/2,$_ IK", "Hello World!"),
        ('B$ L# B$ L" B+ v" v" B* I$ I# v8', 12),
        ('B$ B$ L" B$ L# B$ v" B$ v# v# L# B$ v" B$ v# v# L" L# ? B= v# I! I" B$ L$ B+ B$ v" v$ B$ v" v$ B- v# I" I%', 16)
    ]

def run_tests():
    for token_string, goal in tests:
        print('** running test **')

        expr = TreeExpr.from_token_string(token_string)
        result = None
        try:
            result = eval_expr(expr)
        except:
            print(token_string)
            print(expr)
            print('Failure!')
            raise

        if result != goal:
            print(token_string)
            print(expr)
            print('  evaluated:', result)
            print('  goal:', goal)

def evaluate_string(s):
    return eval_expr(TreeExpr.from_token_string(s))

def repl():
    print([encode_integer(i) for i in range(20)])
    import readline
    try:
        while True:
            token_string = input("lambda-expression>  ")
            print(evaluate_string(token_string))
    except EOFError:
        print()
        pass

def run():
    import sys
    if len(sys.argv) == 1:
        # run_tests()
        repl()
    elif len(sys.argv) == 2:
        command = sys.argv[1]

        if command == 'tests':
            run_tests()
        else:
            print("Unknown command")
        # print(f'Evaluating "{command}"')
        # print(evaluate_string(command))

if __name__ == '__main__':
    run()
