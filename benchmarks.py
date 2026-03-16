
import time

def benchmark(func, *args, **kwargs):
    t1 = time.time()
    r = func(*args, **kwargs)
    t2 = time.time()
    return r, t2 - t1
