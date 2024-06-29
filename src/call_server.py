# import requests
import urllib.request
import time

import expr
import secr

def post_icfp(icfp):
    assert type(icfp) == str
    # result = requests.post(
            # secr.post_url,
            # data = icfp)

    req = urllib.request.Request(
        secr.post_url,
        data = icfp.encode('utf8'),
        headers = {'Authorization': secr.auth},
        method = 'POST')
    with urllib.request.urlopen(req) as response:
        return response.read().decode()
    time.sleep(0.2)

def repl():
    import readline
    try:
        while True:
            text = input("icfp>  ")
            text = text.strip()
            encoded = expr.encode_string(text)
            response = post_icfp(encoded)
            print('Response:', response[:20], response[-20:], len(response), len(response.split()))
            # print('Raw text:', response)
            print(expr.evaluate_string(response))
    except EOFError:
        print()
        pass

# also scoreboard, efficiency
pages = ['index', 'lambdaman', 'spaceship', '3d']
def save_page(page_name):
    response = post_icfp(expr.encode_string('get ' + page_name))
    text = expr.evaluate_string(response)
    with open(f'../pages/{page_name}.md', 'w') as f:
        f.write(text)

def download_lambdaman():
    for i in range(1, 22):
        query = expr.encode_string(f'get lambdaman{i}')
        response = post_icfp(query)
        time.sleep(3)
        print(response[:20])
        with open(f'../input/lambdaman/raw_{i:03}', 'w') as f:
            f.write(response)
            f.write('\n\n')
            f.write(expr.TreeExpr.from_token_string(response).pretty_print())
            f.write('\n')
        if not (i in [10, 21]):
            with open(f'../input/lambdaman/{i:03}', 'w') as f:
                f.write(expr.evaluate_string(response))

if __name__ == '__main__':
    repl()
    # download_lambdaman()
