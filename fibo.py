#fibonacci algorithms

import timeit
import time

template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""

timeit.template = template 

def recursive_fibonacci(n_val):
    if(n_val == 0):
        return 0
    elif(n_val == 1):
        return 1
    else:
        return recursive_fibonacci( n_val - 1 ) + recursive_fibonacci( n_val - 2 )

def non_recursive_fibonacci(n_val):
    a,b = 0,1
    while(n_val > 0):
        a,b = b,a + b
        n_val -= 1
    return a

in_vals = "0\n1\n1\n2\n3\n5\n8\n13\n21\n"

vals = dict()
keys = in_vals.splitlines()

for num in keys:
    if num not in vals:
        #it's a race!
        no_recurs_time, no_recurs_val = timeit.timeit('non_recursive_fibonacci(int(num))', number=1, globals=globals())
        recurse_time, recurs_val = timeit.timeit('recursive_fibonacci(int(num))', number=1, globals=globals())
        if (recurse_time > no_recurs_time):
            vals[num] = no_recurs_val
            print('\nnon recursion was faster calculating: ' + str(num) + '\nresult: ' + str(vals[num]))
        else:
            vals[num] = recurs_val
            print('\nrecursion was faster calculating: ' + str(num) + '\nresult: ' + str(vals[num]))
        print('recursion time: ' + str(recurse_time) + '\nno_recurs_time: ' + str(no_recurs_time))
    else:
        print('\npre-existing in dictionary, not recalcuating: ')
        print(num)
        #vals[num] = 
    