import expr
import call_server
import task

from expr_dsl import *

class Course_LM:
    def __init__(self):
        self.count = 21

    def score(self, solution):
        return len(solution)

    def format_solution(self, solution):
        return solution

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

def solve_6b(task):
    assert task.idx == 6
    body = lam(lambda f:
        f(f(f(f(f(f(S('RRRR'))))))))(
        lam(lambda a: a @ a))

    tree = S('solve lambdaman6 ') @ body
    print(tree.e)
    result = tree.e.to_token_string()
    print(result)
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

def solve_19(task):
    U, D, R, L = S('U'), S('D'), S('R'), S('L')
    assert task.idx == 19
    body = lam(lambda Y:
        Y(lam(lambda foo:
            lam(lambda n :
            lam(lambda r :
            lam(lambda n_ : If(n == zero,
               S(''),
               r(U) @ foo(n_) @ r(D) @ r(L) @ foo(n_) @ r(R) @ r(D) @ foo(n_) @ r(U) @ r(R) @ foo(n_) @ r(L))
            )(n / I(2))
            )(
                lam(lambda c:
                    Y(lam(lambda repeat:
                        lam(lambda k:
                            If(k == one, c, c @ repeat(k - one))
                    )))(n))
            ))
        ))(I(64))
    )(ycomb())

    result = S('solve lambdaman19 ') @ body
    result = result.e.to_token_string()
    # check = expr.evaluate_string(result)
    # print(check)
    # print(len(check))
    # print(len(result))
    task.solve = result

literal_solves = {
            1 : 'UDLLLDURRRRRURR',
            3 : 'DRDRLLLUDLLUURURLLRULUURRDRURRDLDLRDURDD',
            5 : 'RDLLLULURUDRURRRR'
        }

def test():
    # Task(5).display()
    # Task(6).display()
    # Task(9).display()
    t = Task(6)
    solve_6b(t)
    # solve_19(t)
    # t.literal(literal_solves[3])
    t.submit()

    # submit(1, literal(1, 'UDLLLDURRRRRURR'))
    # submit(6, solve_6())
    # submit(9, solve_9())

    # for i in range(1, 22):
        # Task(i).display()

if __name__ == '__main__':
    test()
