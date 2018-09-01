#!/usr/bin/env python3
import math
import functools

def brute_force(factors,n):
    """Simple brute force method of finding the sum"""
    total = 0
    for i in range(n):
        if (any(i % factor == 0 for factor in factors)):
            total+=i
    return total

def build_fast(factors):
    """Computes the lookup table and constants for use in the fast computation, then returns a function which evalutes it"""
    factors=frozenset(factor for factor in factors if all((factor == i) or (factor % i != 0) for i in factors))
    lcm = functools.reduce(lambda a,b: a * b // math.gcd(a,b),factors)
    partials = [None]*lcm
    total = 0
    count = 0
    for i in range(lcm):
        partials[i]=(total,count)
        if(any(i % factor == 0 for factor in factors)):
            total += i
            count += 1
    partials=tuple(partials)
    a = 2 * lcm * count - 2 * total - lcm
    b = 2 * lcm * count - 4 * total - lcm
    def fast(n):
        full,partial = divmod(n,lcm)
        rem,extra = partials[partial]
        return (full * (full * a - b)) // 2 + full * extra * lcm + rem
    return fast

_cache_fast = functools.lru_cache(None)(build_fast)

def fast(factors, n):
    """An uncurried version of build_fast with a cache to avoid rebuilding the inner function"""
    return _cache_fast(frozenset(factors))(n)

def answer():
    """Compute the answer to the problem itself"""
    return fast([3,5],1000)

if __name__ == "__main__":
    print(answer())
