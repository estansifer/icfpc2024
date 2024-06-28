import expr

T = expr.TreeExpr

class E:
    def __init__(self, foo):
        self.e = foo

    def __call__(self, bar):
        return E(T('B$', [self.e, bar.e]))

    def int2str(self):
        return E(T('U$', [self.e]))

    def str2int(self):
        return E(T('U#', [self.e]))

    def op(self, o, bar):
        return E(T('B' + o, [self.e, bar.e]))

    def if_(self, bar, baz):
        return E(T('?', [self.e, bar.e, baz.e]))

    def __neg__(self, bar):
        return E(T('U-', [self.e]))

    # a @ b
    def __matmul__(self, bar):
        return E(T('B.', [self.e, bar.e]))

    def __add__(self, bar):
        return E(T('B+', [self.e, bar.e]))

    def __sub__(self, bar):
        return E(T('B-', [self.e, bar.e]))

    def __mul__(self, bar):
        return E(T('B*', [self.e, bar.e]))

    def __truediv__(self, bar):
        return E(T('B/', [self.e, bar.e]))

    def __mod__(self, bar):
        return E(T('B%', [self.e, bar.e]))

    def __and__(self, bar):
        return E(T('B&', [self.e, bar.e]))

    def __or__(self, bar):
        return E(T('B|', [self.e, bar.e]))

    def __eq__(self, bar):
        return E(T('B=', [self.e, bar.e]))

    def __lt__(self, bar):
        return E(T('B<', [self.e, bar.e]))

    def __gt__(self, bar):
        return E(T('B>', [self.e, bar.e]))

    def __str__(self):
        return str(self.e)

def S(foo):
    return E(T(expr.encode_string(foo), []))

def I(foo):
    return E(T(expr.encode_integer(foo), []))

def If(foo, bar, baz):
    return foo.if_(bar, baz)

true = E(T('T', []))
false = E(T('F', []))
zero = I(0)
one = I(1)

def lam(foo):
    dummy = foo(true)
    vs = list(dummy.e.all_variables())

    idx = 1
    while expr.encode_integer(idx)[1:] in vs:
        idx += 1

    name = expr.encode_integer(idx)[1:]

    return E(T('L' + name, [foo(E(T('v' + name, []))).e]))

def ycomb():
    def outer(x):
        inner = lam(lambda y : x(y(y)))
        return inner(inner)
    return lam(outer)
