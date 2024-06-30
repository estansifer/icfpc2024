import expr

class Course_S:
    def __init__(self):
        self.count = 1

    # evaluate
    # solution is a string consisting of a list of integers
    def score(self, solution):
        return len(solution)

    # create string for submitting to website
    def prepare_submission(self, idx, solution):
        return expr.encode_string(f'solve spaceship{idx} {solution}')

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
    import matplotlib
    matplotlib.use('qtagg')
    import matplotlib.pyplot as plt
    import os.path

    pts = []

    with open(f'../spaceship/levels/{idx}.txt', 'r') as f:
        for line in f:
            x, y = line.split()
            pts.append((int(x), int(y)))

    accs = []

    if acc_file is None:
        acc_file = f'../spaceship/results/levels/{idx}.txt'

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
    plt.show()

def run():
    import sys
    graph(int(sys.argv[1]))

if __name__ == '__main__':
    run()
