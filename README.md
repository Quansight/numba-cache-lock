# numba-lock-cache

## Intro

numba-lock-cache monkey-patch the Numba caching mechanism
smartjit `@jit` decorator adds extra customization of when code execution should fall back to the interpreter. It works as follow:

1. For jitted functions with cache (overloads), use the jitted function if available, and interpreted code otherwise
2. Add a **dispatching** logic, an optional function to pass to the jit decorator, which will decide wether to use jit or not.

## Install

numba-smartjit is available on PyPI and can be installed with the command below:

```bash
pip install numba-smartjit
```

## How to use it

[howto.md](howto.md)


# numba-locking-cache

A Python package that monkey-patches Numba's caching mechanism to safely coordinate concurrent cache access using file locks.

## Why?

Numba’s function-level caching (`@jit(cache=True)`) is not concurrency-safe by default. This can lead to:

- Crashes when multiple processes load/write to the same cache
- Especially problematic on shared filesystems (e.g., NFS)

## Locking Mechanism

- Uses [`flufl.lock`](https://pypi.org/project/flufl.lock/) for file-based locking.
- Lock file is created next to the cache index file:
  `/path/to/cache/func.nbi.lock`
- Lock behavior:
  - Timeout to acquire: 60 seconds (configurable)
  - Lifetime: `None` (lock persists until released)
  - NFS-safe: relies on atomic file creation

## Installation

```bash
pip install numba-locking-cache
```

## How to use it

Just import the patch Numba in your application:

```python
import numba_locking_cache  # triggers monkey patching

from numba import jit

@jit(cache=True)
def my_func(x):
    return x * 2
```