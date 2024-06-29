import expr
import call_server
import task

from expr_dsl import *

class Course_LM:
    def __init__(self):
        self.count = 21

    def score(self, solution):
        return len(solution)

    def prepare_submission(self, idx, solution):
        return solution

class Task:
    def __init__(self, idx):
        self.idx = idx
        self.board = None
        self.nrow = None
        self.ncol = None
        self.solve = None

        # if not (idx in [10, 21]):
        if True:
            self.board = []
            with open(f'../input/lambdaman/{idx:03d}', 'r') as f:
                for line in f:
                    line = line.strip()
                    if len(line) > 0:
                        self.board.append(line)
            self.nrow = len(self.board)
            self.ncol = len(self.board[0])

    def literal(self, moves):
        self.solve = expr.encode_string(f'solve lambdaman{self.idx} {moves}')
        return self.solve

    def submit(self):
        if not (self.solve is None):
            task.submit('lambdaman', self.idx, self.solve)

    def display(self):
        import matplotlib
        matplotlib.use('qtagg')
        import matplotlib.pyplot as plt
        import numpy as np

        g = np.zeros((self.nrow, self.ncol), dtype = int)
        for i in range(self.nrow):
            for j in range(self.ncol):
                g[i, j] = (self.board[i][j] == '#')

        plt.clf()
        plt.imshow(g)
        plt.axis('equal')
        plt.show()

def solve_6(task):
    assert task.idx == 6
    f = lam(lambda a:
        lam(lambda b:
            If((b == one),
               S('R'),
               S('R') @ (a(b - one)))))

    tree = S('solve lambdaman6 ') @ (ycomb()(f)(I(199)))
    result = tree.e.to_token_string()
    task.solve = result

def solve_9(task):
    assert task.idx == 9
    repeat = lam(lambda a:
        ycomb()(
            lam(lambda b: lam(lambda c:
                If(c == one, a, a @ b(c - one))))))

    f = lam(lambda r:
            r(
                r(S('R'))(I(50)) @ r(S('L'))(I(50)) @ S('D')
            )(I(50)))
    result = S('solve lambdaman9 ') @ f(repeat)
    result = result.e.to_token_string()
    task.solve = result

literal_solves = {
            1 : 'UDLLLDURRRRRURR',
            3 : 'DRDRLLLUDLLUURURLLRULUURRDRURRDLDLRDURDD'
        }

def test():
    Task(10).display()
    Task(21).display()
    # t = Task(3)
    # t.literal(literal_solves[3])
    # t.submit()

    # submit(1, literal(1, 'UDLLLDURRRRRURR'))
    # submit(6, solve_6())
    # submit(9, solve_9())

    # for i in range(1, 22):
        # if not i in [10, 21]:
            # Task(i).display()

if __name__ == '__main__':
    test()
