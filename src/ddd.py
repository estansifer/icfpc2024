import call_server
import task
import expr
import readline

class Course_3D:
    def __init__(self):
        self.count = 12

    def score(self, solution):
        return None

    def format_solution(self, solution):
        return solution

    def prepare_submission(self, idx, solution):
        return expr.encode_string(f'solve 3d{idx}\n' + solution + '\n')

def submit(idx):
    with open(f'../output/3d/{idx:03}', 'r') as f:
        solve = f.read().strip()

    task.submit('3d', idx, solve)

def test_taylor(A = None, F = 10 ** 9, max_n = 17, verbose = False):
    import math

    def sin(x):
        n = 1
        x_n = x
        accum = 0
        fact = 1
        F_n = 1

        while n < max_n:
            if verbose:
                print('**** new step ****')
                print('n', n)
                print('x ^ n', x_n)
                print('accum', accum)
                print('fact', fact)
                print('F_n', F_n)
            accum = F * n * accum + (n % 2) * ((n % 4) - 2) * x_n
            x_n = x * x_n
            F_n = F * F_n
            fact = n * fact
            n = n + 1

        return - (((accum * F) // F_n) // fact)

    def sin2(x):
        a = 1
        b = 1
        c = 1
        d = 1
        e = 1
        f = 0
        g = 0

        while a < max_n:
            if verbose:
                print('**** new step ****')
                print('a: n + 1', a)
                print('b: x ^ n', b)
                print('g: accum', g)
                print('e: fact', e)
                print('d: F_n', d)
            f, g = g, b * 99 // (e * d) - f
            e = a * e
            d = c * d
            c = F
            b = x * b
            a = a + 1

        return g // (-99)

    if A is None:
        import numpy as np
        def check(x):
            a = int(math.sin(x) * F)
            b = sin2(int(x * F))
            print(a, b, a - b)

        # for x in np.linspace(-1.6, 1.6, 200):
        for x in [-1, -0.5, 0, 0.5, 1]:
            check(x)
    else:
        ra = sin2(int(A))
        rb = int(math.sin(A / F) * F)
        return (ra, rb, ra - rb)

def grid_print(grid):
    nrow = len(grid)
    ncol = len(grid[0])

    widths = [1] * ncol

    output = [[None] * ncol for i in range(nrow)]

    for row in range(nrow):
        for col in range(ncol):
            if grid[row][col] is None:
                output[row][col] = ' .'
            else:
                output[row][col] = ' ' + str(grid[row][col])
                widths[col] = max(widths[col], len(output[row][col]))

    for row in range(nrow):
        for col in range(ncol):
            while len(output[row][col]) < widths[col]:
                output[row][col] = ' ' + output[row][col]

    for row in output:
        print(''.join(row))

def simulate(grid, verbose = False, maxsteps = 100):
    nrow = len(grid)
    ncol = len(grid[0])

    def copy_grid(gss):
        return [gs[:] for gs in gss]

    def empty_grid(fill = None):
        return [[fill] * ncol for i in range(nrow)]

    timeline = [None, copy_grid(grid)]

    dirs = {
        '>' : (0, 1),
        '<' : (0, -1),
        'v' : (1, 0),
        '^' : (-1, 0)
            }

    # edits timeline in place
    def step():
        t = len(timeline) - 1
        gss = timeline[-1]
        newgrid = empty_grid()
        still = empty_grid(True)

        next_time = None

        for row in range(nrow):
            for col in range(ncol):
                o = gss[row][col]
                if (o is None) or (type(o) is int):
                    continue
                if o == '@':
                    dx = gss[row][col - 1]
                    dy = gss[row][col + 1]
                    dt = gss[row + 1][col]
                    obj = gss[row - 1][col]
                    if (
                            (type(dx) is int) and
                            (type(dy) is int) and
                            (type(dt) is int) and
                            (not (obj is None))):
                        if next_time is None:
                            next_time = t - dt
                            assert next_time >= 1
                            assert dt >= 1
                        assert next_time == t - dt
                        timeline[next_time][row - dy][col - dx] = obj
                elif o in '<>v^':
                    drow, dcol = dirs[o]
                    obj = gss[row - drow][col - dcol]
                    if not (obj is None):
                        still[row - drow][col - dcol] = False
                        assert newgrid[row + drow][col + dcol] == None
                        newgrid[row + drow][col + dcol] = obj
                elif o in '+-*/%=#':
                    obj1 = gss[row][col - 1]
                    obj2 = gss[row - 1][col]
                    if None in [obj1, obj2]:
                        continue
                    out1 = None
                    out2 = None
                    if o == '=':
                        if obj1 == obj2:
                            out1 = obj1
                            out2 = obj2
                    elif o == '#':
                        if obj1 != obj2:
                            out1 = obj1
                            out2 = obj2
                    elif (type(obj1) is int) and (type(obj2) is int):
                        if o == '+':
                            out = obj1 + obj2
                        elif o == '-':
                            out = obj1 - obj2
                        elif o == '*':
                            out = obj1 * obj2
                        elif o == '/':
                            out = obj1 // obj2
                        elif o == '%':
                            out = obj1 % obj2
                        else:
                            assert False
                        out1 = out
                        out2 = out
                    if not (out1 is None):
                        still[row - 1][col] = False
                        still[row][col - 1] = False
                        assert newgrid[row + 1][col] == None
                        assert newgrid[row][col + 1] == None
                        newgrid[row + 1][col] = out1
                        newgrid[row][col + 1] = out2


        output = None
        for row in range(nrow):
            for col in range(ncol):
                if still[row][col] and (gss[row][col] == 'S'):
                    if not (newgrid[row][col] is None):
                        assert output in [newgrid[row][col], None]
                        output = newgrid[row][col]

                if newgrid[row][col] is None:
                    if still[row][col]:
                        newgrid[row][col] = gss[row][col]

        if next_time is None:
            timeline.append(newgrid)
        else:
            while len(timeline) > next_time + 1:
                timeline.pop()

        if not (output is None):
            if verbose:
                print('Output:', output)
            return output

    if verbose:
        try:
            while True:
                grid_print(timeline[-1])
                print('t = ', len(timeline) - 1)

                x = input('> ')
                step()
        except EOFError:
            print()
            pass
    else:
        for i in range(maxsteps):
            output = step()
            if not (output is None):
                return output

def read_grid(idx, A, B):
    rows = []
    ncols = 0
    with open(f'../output/3d/{idx:03}', 'r') as f:
        for line in f:
            cols = line.strip().split()
            ncols = max(ncols, len(cols))
            for i in range(len(cols)):
                if cols[i] == '.':
                    cols[i] = None
                if cols[i] == 'A':
                    cols[i] = A
                if cols[i] == 'B':
                    cols[i] = B
                try:
                    cols[i] = int(cols[i])
                except:
                    pass
            rows.append(cols)

    for row in rows:
        while len(row) < ncols:
            row.append(None)

    return rows

def test():
    A = 1621823881
    for A in [-1612893, -1621823881, 1621823881, 0, 20, 1, -1, 1000324]:
        # A = 58
        g = read_grid(12, A, 0)
        F = 10 ** 9
        # F = 64
        max_n = 17
        tt = test_taylor(A, F, max_n)
        print('A:', A)
        print('F:', F)
        print('max n:', max_n)
        print('Simulation result:', simulate(g))
        print('formula result:', tt[0])
        print('sine:', tt[1], tt[2])

        # test_taylor(A, B, max_n, verbose = True)

        # simulate(g, verbose = True)

def run():
    submit(12)
    # test()
    # submit(9)
    # test_taylor()
    # submit(1)

    # g = read_grid(1, 1, 0)
    # simulate(g, verbose = True)

if __name__ == '__main__':
    run()
