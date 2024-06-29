import call_server
import task
import expr

class Course_3D:
    def __init__(self):
        self.count = 12

    def score(self, solution):
        return None

    def prepare_submission(self, idx, solution):
        return expr.encode_string(f'solve 3d{idx}\n' + solution + '\n')

def submit(idx):
    with open(f'../output/3d/{idx:03}', 'r') as f:
        solve = f.read().strip()

    task.submit('3d', idx, solve)

def run():
    submit(6)

if __name__ == '__main__':
    run()
