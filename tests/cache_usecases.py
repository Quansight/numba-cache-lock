from numba import jit

from numba_cache_lock import patch_numba_cache

patch_numba_cache()


@jit(cache=True, nopython=True)
def add_fn_usecase(x, y):
    return x + y


@jit(cache=True, nopython=True)
def incr_fn_usecase(x):
    return x + 1
