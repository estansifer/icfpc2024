import call_server
import task
import expr

class Course_Efficiency:
    def __init__(self):
        self.count = 13

    def score(self, solution):
        return 1

    def prepare_submission(self, idx, solution):
        return expr.encode_string(f'solve efficiency{idx} {solution}')

def fib(k):
    f = [1] * 100
    for i in range(2, 100):
        f[i] = f[i - 1] + f[i - 2]
    return f[k]

answers = [
        'zero index',
        4 ** 22, # 1
        2134, # 2
        2134 + 9345873499 + 1, # 3
        fib(40), # 4
        2 ** 31 - 1, # 5, calculates first mersenne prime above 1000000
        42, # 6, calculates first fibonacci prime starting from fib(30)
        None, # 7
        None, # 8
        None, # 9
        None, # 10
        None, # 11
        (127 - 1) * (9721 - 1) + 1, # 12
        2 ** 29 + 7  # 13
    ]

def submit(idx):
    assert type(answers[idx]) == int
    task.submit('efficiency', idx, str(answers[idx]))

def run():
    pass

if __name__ == '__main__':
    run()
