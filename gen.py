from math import pi, sin, cos

def GEN1(params):
    assert(len(params)%2 == 0)
    return ([params[j] + (params[j+2] - params[j])*(i - params[j+1])/(params[j+3] - params[j+1]) 
        for j in range(0, len(params)-2, 2) for i in range(int(params[j+1]), int(params[j+3]))])

def GEN2(params, FUNCTION_LEN):
    N = params[-1]
    P = FUNCTION_LEN
    function = [sum([params[k]*sin(2*pi*(k+1)*i/(P-1)) for k in range(abs(N))])
        + sum([params[abs(N) + k]*cos(2*pi*k*i/(P-1)) for k in range(len(params) - abs(N) - 1)])
        for i in range(P)]
    if N > 0:
        function /= max(function)
    return function

def GEN3(params, FUNCTION_LEN):
    interval_count = len(params) - 1
    remainder = FUNCTION_LEN % interval_count
    return [params[j] + (params[j+1] - params[j])*(i/(interval_len := FUNCTION_LEN//interval_count + 
        (1 if j < remainder else 0))) for j in range(interval_count) for i in range(interval_len)]
