from pathlib import Path
import call_server
import expr
import sys
import time

for path in Path(sys.argv[1]).rglob('*.txt'):
    with path.open() as f:
        contents = f.read()
    request = f'solve spaceship{path.stem} {contents}'
    print(request)
    print(expr.evaluate_string(call_server.post_icfp(expr.encode_string(request))))
    time.sleep(5)
