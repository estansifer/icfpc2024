import call_server
from collections import deque
import expr
from expr_dsl import *
import functools
import operator
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
    def sim(self, steps, previous_state=None):
        if previous_state is not None:
            x = previous_state[0]
            y = previous_state[1]
            rows = self.rows
            pellets_left = previous_state[2]
            pellets_taken = set(previous_state[3])
        else:
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
        return (x, y, pellets_left, pellets_taken)
    def distance_squared_to_closest_pellet(self, state):
        lx = state[0]
        ly = state[1]
        pellets_taken = state[3]
        min_distance_squared = 9999999999
        for y in range(len(self.rows)):
            for x in range(len(self.rows[y])):
                if self.rows[y][x] == '.' and (x, y) not in pellets_taken:
                    dx = lx - x
                    dy = ly - y
                    d2 = dx * dx + dy * dy
                    if d2 < min_distance_squared:
                        min_distance_squared = d2
        return min_distance_squared
    def steps_to_closest_pellet(self, state):
        lx = state[0]
        ly = state[1]
        pellets_taken = state[3]
        height = len(self.rows)
        width = len(self.rows[0])
        lengths = [99999999] * width * height
        lengths[ly * width + lx] = 0
        queue = deque([(lx, ly)])
        while len(queue) > 0:
            x, y = queue.popleft()
            length = lengths[y * width + x]
            if self.rows[y][x] == '.' and (x, y) not in pellets_taken:
                return length
            if y > 0 and self.rows[y - 1][x] != '#' and length + 1 < lengths[(y - 1) * width + x]:
                lengths[(y - 1) * width + x] = length + 1
                queue.append((x, y - 1))
            if y < len(self.rows) - 1 and self.rows[y + 1][x] != '#' and length + 1 < lengths[(y + 1) * width + x]:
                lengths[(y + 1) * width + x] = length + 1
                queue.append((x, y + 1))
            if x > 0 and self.rows[y][x - 1] != '#' and length + 1 < lengths[y * width + x - 1]:
                lengths[y * width + x - 1] = length + 1
                queue.append((x - 1, y))
            if x < len(self.rows[y]) - 1 and self.rows[y][x + 1] != '#' and length + 1 < lengths[y * width + x + 1]:
                lengths[y * width + x + 1] = length + 1
                queue.append((x + 1, y))
        return 99999999

params = 'glibc_udlr'

if params == 'random0':
    # parameters via 'random0' (https://www1.udel.edu/CIS/106/pconrad/MPE3/code/chap5/random0.m)
    func = lam(lambda f: lam(lambda steps: lam(lambda state:
        (steps > I(0)).if_(
            S("UDRL").drop((state + state / I(2351)) % I(4)).take(I(1)) @ f(f)(steps - I(1))((state * I(8121) + I(28411)) % I(134456)),
            S("")
        )
    )))
    def pyfunc(state, steps):
        result = ''
        for _ in range(steps):
            result += 'UDRL'[(state + state // 2351) % 4]
            state = (state * 8121 + 28411) % 134456
        return result
elif params == 'glibc':
    func = lam(lambda f: lam(lambda steps: lam(lambda state:
        (steps > I(0)).if_(
            S("UDRL").drop((state + state / I(22351)) % I(4)).take(I(1)) @ f(f)(steps - I(1))((state * I(1103515245) + I(12345)) % I(2 ** 31)),
            S("")
        )
    )))
    def pyfunc(state, steps):
        result = ''
        for _ in range(steps):
            result += 'UDRL'[(state + state // 22351) % 4]
            state = (state * 1103515245 + 12345) % (2 ** 31)
        return result
elif params == 'glibc_udlr':
    func = lam(lambda f: lam(lambda steps: lam(lambda state:
        (steps > I(0)).if_(
            S("UDLR").drop((state + state / I(22351)) % I(4)).take(I(1)) @ f(f)(steps - I(1))((state * I(1103515245) + I(12345)) % I(2 ** 31)),
            S("")
        )
    )))
    def pyfunc(state, steps):
        result = ''
        for _ in range(steps):
            result += 'UDLR'[(state + state // 22351) % 4]
            state = (state * 1103515245 + 12345) % (2 ** 31)
        return result

def submit_seeds(idx, steps_per_seed, seeds):
    call = lam(lambda g:
        lam(lambda f:
            functools.reduce(operator.matmul, map(lambda seed: f(I(seed)), seeds))
        )(g(g)(I(steps_per_seed)))
    )(func)
    token_string = (S(f'solve lambdaman{idx} ') @ call).e.to_token_string()
    print(token_string)
    task.submit('lambdaman', idx, token_string)

for idx in range(1, 22):
    seeds = []
    try:
        with open(f'../lcg-seeds/100000_20000/{idx:03d}', 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) > 0:
                    seeds.append(int(line))
        if len(seeds) > 0:
            submit_seeds(idx, 20000, seeds)
    except:
        pass
exit()

submit_seeds(8, 100000, [13628, 83757, 22430, 87629, 33908, 0])
exit()

steps_per_seed = 8835
seeds_to_try = 8836

steps_for_seed = [pyfunc(seed, steps_per_seed) for seed in range(seeds_to_try)]

for idx in range(8, 9):
    try:
        board = Board(idx)
    except:
        continue
    print('looking at', idx)
    seeds = []
    total_steps = 0
    state = None
    while total_steps < 1000000 and (state is None or state[2] > 0):
        min_seed = 0
        min_next_state = None
        min_steps = 9999999999
        for seed in range(seeds_to_try):
            next_state = board.sim(steps_for_seed[seed], previous_state=state)
            if min_next_state is None or next_state[2] < min_next_state[2] or (next_state[2] == min_next_state[2] and board.steps_to_closest_pellet(next_state) < min_steps):
                min_next_state = next_state
                min_seed = seed
                min_steps = board.steps_to_closest_pellet(next_state)
                print(seed, board.pellets, next_state[2], min_steps)
                if next_state[2] == 0:
                    break
        seeds.append(min_seed)
        state = min_next_state
        total_steps += steps_per_seed
    if state[2] == 0:
        submit_seeds(idx, steps_per_seed, seeds)
