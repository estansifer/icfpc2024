import call_server
import task
import expr

class Course_Efficiency:
    def __init__(self):
        self.count = 13

    def score(self, solution):
        return 1

    def format_solution(self, solution):
        return solution

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

def deduce(N, conds_, guesses, deductions = None):
    if deductions is None:
        ded_yes = 0
        ded_no = 0
        for k, sign in guesses:
            if sign == 1:
                ded_yes = ded_yes + (2 ** k)
            else:
                ded_no = ded_no + (2 ** k)
    else:
        ded_yes, ded_no, _ = deductions

    conds = list(conds_)

    flag = True
    while flag:
        flag = False

        for cond in list(conds):
            y, n = cond

            fails = (y & ded_no) | (n & ded_yes)
            k = fails.bit_count()
            # Failed?
            if k == 3:
                return False

            # Neutral?
            if (y & ded_yes) == (n & ded_no): # == 0
                # up to 2?
                if k == 2:
                    flag = True
                    other = (y + n) - fails

                    if (other & y) > 0:
                        ded_yes = ded_yes | other
                    else:
                        ded_no = ded_no | other
            else:
                # passed!
                conds.remove(cond)
                flag = True

        if len(conds) == 0:
            return (ded_yes, ded_no, True)

    return (ded_yes, ded_no, False)

def sat(idx):
    l = None
    with open(f'../input/efficiency/raw_{idx:03}', 'r') as f:
        for line in f:
            l = line.strip()
            break

    # print(l)

    te = expr.TreeExpr.from_token_string(l)

    def foo(e):
        if e.token == 'B$' and e.args[1].size < 50:
            print(e.args[0].token, ': ', e.args[1].pretty_print())

        if e.token == '?':
            print(e.token, e.size, e.args[0].size, e.args[1].size, e.args[2].size)
            print(e.pretty_print())

    te.walk(foo)




def submit(idx):
    assert type(answers[idx]) == int
    task.submit('efficiency', idx, str(answers[idx]))

def run():
    sat(7)

if __name__ == '__main__':
    run()
