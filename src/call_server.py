# import requests
import urllib.request

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

def repl():
    import readline
    try:
        while True:
            text = input("icfp>  ")
            text = text.strip()
            encoded = expr.encode_string(text)
            response = post_icfp(encoded)
            print('Raw text:', response)
            print(expr.evaluate_string(response))
    except EOFError:
        print()
        pass

if __name__ == '__main__':
    repl()
