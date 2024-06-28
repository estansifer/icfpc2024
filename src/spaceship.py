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
