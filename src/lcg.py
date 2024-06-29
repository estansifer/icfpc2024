import call_server
import expr
from expr_dsl import *
import task

# parameters via 'random0' (https://www1.udel.edu/CIS/106/pconrad/MPE3/code/chap5/random0.m)
func = lam(lambda state: lam(lambda steps: lam(lambda f:
    (steps > I(0)).if_(
        S("UDRL").drop((state + state / I(2351)) % I(4)).take(I(1)) @ f((state * I(8121) + I(28411)) % I(134456))(steps - I(1))(f),
        S("")
    )
)))

call = lam(lambda g: g(I(1))(I(1000000))(g))(func)

idx = 4

token_string = (S(f'solve lambdaman{idx} ') @ call).e.to_token_string()

print(token_string)

task.submit('lambdaman', idx, token_string)