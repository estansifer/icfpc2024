import requests

import expr
import secr

def post_icfp(icfp):
    assert type(icfp) == str
    result = requests.post(
            secr.post_url)
