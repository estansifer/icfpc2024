import call_server
import expr
from expr_dsl import *
import task

class Board:
    def __init__(self, idx):
        self.rows = []
        self.lx = -1
        self.ly = -1
        self.pellets = 0
        with open(f'../input/lambdaman/{idx:03d}', 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) > 0:
                    try:
                        self.lx = line.index('L')
                        self.ly = len(self.rows)
                    except:
                        pass
                    self.pellets += line.count('.')
                    self.rows.append(line)
    def sim(self, steps):
        x = self.lx
        y = self.ly
        rows = self.rows
        pellets_left = self.pellets
        pellets_taken = set()
        for step in steps:
            nx = x
            ny = y
            if step == 'U':
                if ny > 0:
                    ny -= 1
            elif step == 'D':
                if ny < len(rows) - 1:
                    ny += 1
            elif step == 'L':
                if nx > 0:
                    nx -= 1
            elif step == 'R':
                if nx < len(rows[ny]) - 1:
                    nx += 1
            destination = rows[ny][nx]
            if destination != '#':
                x = nx
                y = ny
                if destination == '.' and (x, y) not in pellets_taken:
                    pellets_left -= 1
                    pellets_taken.add((x, y))
        return pellets_left

params = 'glibc'

if params == 'random0':
    # parameters via 'random0' (https://www1.udel.edu/CIS/106/pconrad/MPE3/code/chap5/random0.m)
    func = lam(lambda state: lam(lambda steps: lam(lambda f:
        (steps > I(0)).if_(
            S("UDRL").drop((state + state / I(2351)) % I(4)).take(I(1)) @ f((state * I(8121) + I(28411)) % I(134456))(steps - I(1))(f),
            S("")
        )
    )))
    def pyfunc(state, steps):
        result = ''
        for _ in range(steps):
            result += 'UDRL'[(state + state // 2351) % 4]
            state = (state * 8121 + 28411) % 134456
        return (result, state)
elif params == 'glibc':
    func = lam(lambda state: lam(lambda steps: lam(lambda f:
        (steps > I(0)).if_(
            S("UDRL").drop((state + state / I(22351)) % I(4)).take(I(1)) @ f((state * I(1103515245) + I(12345)) % I(2 ** 31))(steps - I(1))(f),
            S("")
        )
    )))
    def pyfunc(state, steps):
        result = ''
        for _ in range(steps):
            result += 'UDRL'[(state + state // 22351) % 4]
            state = (state * 1103515245 + 12345) % (2 ** 31)
        return (result, state)

idx = 18
board = Board(idx)
for seed in range(1000):
    steps, _ = pyfunc(seed, 1000000)
    result = board.sim(steps)
    print(seed, board.pellets, result)
    if result == 0:
        call = lam(lambda g: g(I(seed))(I(1000000))(g))(func)
        token_string = (S(f'solve lambdaman{idx} ') @ call).e.to_token_string()
        print(token_string)
        task.submit('lambdaman', idx, token_string)
        break
