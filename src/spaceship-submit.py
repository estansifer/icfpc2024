from pathlib import Path
import call_server
import expr
from expr_dsl import *
import sys
import task

def encode(encode_run):
    e = S("")
    unencoded = ''
    run = None
    runlength = 0
    for c in contents:
        # print(e.e.to_token_string())
        if run is None:
            run = c
            runlength = 1
        elif c == run:
            runlength += 1
        elif runlength < 25:
            unencoded += run * runlength
            run = c
            runlength = 1
        else:
            if len(unencoded) > 0:
                e = e @ S(unencoded)
            e = e @ encode_run(S(run))(I(runlength))
            unencoded = ''
            run = c
            runlength = 1
    if runlength < 25:
        unencoded += run * runlength
        e = e @ S(unencoded)
    else:
        if len(unencoded) > 0:
            e = e @ S(unencoded)
        e = e @ encode_run(S(run))(I(runlength))
    return e

for path in Path(sys.argv[1]).rglob('*.txt'):
    with path.open() as f:
        contents = f.read()
    result = lam(encode)(ycomb()(
        lam(lambda f: lam(lambda s: lam(lambda n:
            (n == I(1)).if_(
                s,
                s @ f(s)(n - I(1))
            )
        )))
    ))
    print(len(contents), len(result.e.to_token_string()))
    task.submit('spaceship', int(path.stem), result)
