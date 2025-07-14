import multiprocessing
import os
import unittest

from numba.tests.test_caching import DispatcherCacheUsecasesTest


class TestCacheLock(DispatcherCacheUsecasesTest):
    here = os.path.dirname(__file__)
    usecases_file = os.path.join(here, "cache_usecases.py")

    def test_caching(self):
        self.check_pycache(0)
        mod = self.import_module()
        self.check_pycache(0)

        f = mod.add_fn_usecase
        self.assertPreciseEqual(f(2, 3), 5)
        self.check_pycache(2)  # 1 index, 1 data

    def test_multiprocessing(self):
        # Check caching works from multiple processes at once (#2028)
        mod = self.import_module()
        # Calling a pure Python caller of the JIT-compiled function is
        # necessary to reproduce the issue.
        f = mod.incr_fn_usecase
        n = 3
        try:
            ctx = multiprocessing.get_context("spawn")
        except AttributeError:
            ctx = multiprocessing
        pool = ctx.Pool(n)
        args = range(n)
        try:
            res = sum(pool.imap(f, args))
        finally:
            pool.close()
        self.assertEqual(res, sum(range(n)) + n)


if __name__ == "__main__":
    unittest.main()
