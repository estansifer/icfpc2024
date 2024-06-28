import os
import time

import expr
import call_server
import lambdaman
import spaceship

courses = {}

def init_courses():
    if len(courses) == 0:
        courses['lambdaman'] = lambdaman.Course_LM()
        courses['spaceship'] = spaceship.Course_S()

# solutions
# /output/<course>/solve_{idx:04}_{score}
# /output/<course>/response_{idx:04}_{score}

def view_scores(course = None):
    init_courses()

    if course is None:
        for course in courses:
            view_scores(course)
    else:
        print(f"Our scores for {course}:")
        c = courses[course]
        N = c.count
        best_scores = [None] * N
        comments = [''] * N

        names = os.listdir(f'../output/{course}')
        for name in names:
            if name.startswith('solve_'):
                n1, n2, n3 = name.strip().split('_')
                idx = int(n2) - 1
                score = int(n3)
                if (best_scores[idx] is None) or (best_scores[idx] < score):
                    best_scores[idx] = score
                    if f'response_{idx + 1:04}_{score}' in names:
                        with open(f'../output/{course}/response_{idx + 1:04}_{score}', 'r') as f:
                            comments[idx] = f.read().strip()
                    else:
                        comments[idx] = 'No server response'

        noscores = []
        for idx in range(c.count):
            if best_scores[idx] is None:
                noscores.append(idx)
            else:
                print(f'  Task {idx+1:4}:  {best_scores[idx]:6}  {comments[idx]}')

        if len(noscores) == 1:
            print(f"  No submission for task {noscores[0]+1}.")
        elif len(noscores) > 1:
            print("  No submission for tasks: " + ', '.join([str(idx + 1) for idx in noscores]))

def submit(course, idx, solution, check_if_better_exists = True):
    init_courses()

    c = courses[course]
    score = int(c.score(solution))

    if check_if_better_exists:
        prefix = f'solve_{idx:04}_'
        names = os.listdir(f'../output/{course}')
        best_score = None
        for name in names:
            if name.startswith(prefix):
                score_ = int(name[len(prefix):])
                if score_ <= score:
                    print(f"There is already a submission with score {score_}, which is at least as good as {score}, so skipping submission!")
                    return
                if (best_score is None) or (score_ < best_score):
                    best_score = score_
        print(f"Score {score} is better than best so far {best_score}, submitting!")
    else:
        print(f"Submitting with a score of {score}.")

    with open(f'../output/{course}/solve_{idx:04}_{score}', 'w') as f:
        f.write(solution)
        f.write('\n')

    icfp = c.prepare_submission(idx, solution)
    response = call_server.post_icfp(icfp)

    try:
        response = expr.evaluate_string(response)
    except:
        print('Failed to parse server response!')
        raise
    finally:
        print(response)
        with open(f'../output/{course}/response_{idx:04}_{score}', 'w') as f:
            f.write(response)
            f.write('\n')

    time.sleep(2)

def run():
    init_courses()
    view_scores('lambdaman')

if __name__ == '__main__':
    run()

