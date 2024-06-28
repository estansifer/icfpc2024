import expr
import call_server
import task

class Course_LM:
    def __init__(self):
        self.count = 21

    def score(self, solution):
        return len(solution)

    def prepare_submission(self, idx, solution):
        return solution

# "solve lambdamanX path"

def literal(idx, moves):
    solution = expr.encode_string(f'solve lambdaman{idx} {moves}')
    return solution

def submit_6():
    t = expr.encode_string('solve lambdaman6 ')
    R = expr.encode_string('R')
    s = f'B. {t} B$ B$ L" B$ L" B$ L# B$ v" B$ v# v# L# B$ v" B$ v# v# L$ L# ? B= v# I" v" B. v" B$ v$ B- v# I" {R} I#,'
    print(s)
    submit(6, s)

def test():
    task.submit('lambdaman', 1, literal(1, 'UDLLLDURRRRRURR'))

    # submit_plain_path(1, 'UDLLLDURRRRRURR')
    # submit_plain_path(2, 'RDURRDDRRUUDDLLLDLLDDRRRUR')
    # submit_6()

if __name__ == '__main__':
    test()
