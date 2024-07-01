import expr
from expr_dsl import *

class Course_S:
    def __init__(self):
        self.count = 1

    # evaluate
    # solution is a string consisting of a list of integers
    def score(self, solution):
        # return len(expr.eval_expr_inplace(solution.e))
        return None

    def format_solution(self, solution):
        return solution.e.to_token_string()

    # create string for submitting to website
    def prepare_submission(self, idx, solution):
        return (S(f'solve spaceship{idx} ') @ solution).e.to_token_string()

acc_code = {
        '1' : (-1, -1),
        '2' : ( 0, -1),
        '3' : ( 1, -1),
        '4' : (-1,  0),
        '5' : ( 0,  0),
        '6' : ( 1,  0),
        '7' : (-1,  1),
        '8' : ( 0,  1),
        '9' : ( 1,  1)
    }

def graph(idx, acc_file = None):
    raw_idx = idx
    if idx[-1] == 'a':
        folder = '../spaceship/results/levels/'
        idx = int(idx[:-1])
    elif idx[-1] == 'b':
        folder = '../spaceship/results/tweak/levels/'
        idx = int(idx[:-1])
    else:
        idx = int(idx)
        folder = '../spaceship/results/tweak-factor-0.25/levels/'

    import matplotlib
    # matplotlib.use('qtagg')
    matplotlib.use('agg')
    import matplotlib.pyplot as plt
    import os.path

    pts = []

    with open(f'../spaceship/levels/{idx}.txt', 'r') as f:
        for line in f:
            x, y = line.split()
            pts.append((int(x), int(y)))

    accs = []

    if acc_file is None:
        acc_file = folder + f'{idx}.txt'

    if not (acc_file is None):
        if os.path.exists(acc_file):
            with open(acc_file, 'r') as f:
                accs = f.read().strip()

    path = []
    x, y = 0, 0
    vx, vy = 0, 0
    path.append((x, y))
    for a in accs:
        ax, ay = acc_code[a]
        vx += ax
        vy += ay
        x += vx
        y += vy
        path.append((x, y))

    plt.clf()
    plt.scatter([x for x, y in pts], [y for x, y in pts])
    plt.plot([x for x, y in path], [y for x, y in path])
    plt.savefig(f'../output/spaceship/figs/{raw_idx}.png', dpi = 200)

def run():
    import sys
    for i in range(1, 24):
        graph(str(i))
        graph(str(i) + 'a')
        graph(str(i) + 'b')

if __name__ == '__main__':
    run()
