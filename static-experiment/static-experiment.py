import random
import itertools

def partitions(n, k=None):
    """Generate all partitions of integer n (>= 0) using integers no
    greater than k (default, None, allows the partition to contain n).

    Each partition is represented as a multiset, i.e. a dictionary
    mapping an integer to the number of copies of that integer in
    the partition.  For example, the partitions of 4 are {4: 1},
    {3: 1, 1: 1}, {2: 2}, {2: 1, 1: 2}, and {1: 4} corresponding to
    [4], [1, 3], [2, 2], [1, 1, 2] and [1, 1, 1, 1], respectively.
    In general, sum(k * v for k, v in a_partition.iteritems()) == n, and
    len(a_partition) is never larger than about sqrt(2*n).

    Note that the _same_ dictionary object is returned each time.
    This is for speed:  generating each partition goes quickly,
    taking constant time independent of n. If you want to build a list
    of returned values then use .copy() to get copies of the returned
    values:

    >>> p_all = []
    >>> for p in partitions(6, 2):
    ...         p_all.append(p.copy())
    ...
    >>> print p_all
    [{2: 3}, {1: 2, 2: 2}, {1: 4, 2: 1}, {1: 6}]

    Reference
    ---------
    Original version taken from Chris Smith's posting:
    http://code.activestate.com/recipes/218332/
    ---------
    Modified from Tim Peter's posting to accomodate a k value:
    http://code.activestate.com/recipes/218332/
    ---------
    """
    if n < 0:
        raise ValueError("n must be >= 0")

    if n == 0:
        yield {}
        return

    if k is None or k > n:
        k = n

    q, r = divmod(n, k)
    ms = {k : q}
    keys = [k]
    if r:
        ms[r] = 1
        keys.append(r)
    yield ms

    while keys != [1]:
        # Reuse any 1's.
        if keys[-1] == 1:
            del keys[-1]
            reuse = ms.pop(1)
        else:
            reuse = 0

        # Let i be the smallest key larger than 1.  Reuse one
        # instance of i.
        i = keys[-1]
        newcount = ms[i] = ms[i] - 1
        reuse += i
        if newcount == 0:
            del keys[-1], ms[i]

        # Break the remainder into pieces of size i-1.
        i -= 1
        q, r = divmod(reuse, i)
        ms[i] = q
        keys.append(i)
        if r:
            ms[r] = 1
            keys.append(r)

        yield ms

def relistify(multiset, m):
    setlist = [[k] * multiset[k] for k in multiset]
    setlist.append([0])
    flatlist = list(itertools.chain(*setlist))
    return [2 + flatlist[min(i,len(flatlist)-1)] for i in range(m)]

def main():
    n = 100
    m = 25
    p_all = []
    for p in partitions(n - 2*m, m):
        p_all.append(p.copy())
        
    exp_ks = random.sample(p_all, 100)
    test_k = relistify(exp_ks[0], m)
    print exp_ks[0], test_k, sum(test_k)
    
    
if __name__=="__main__":
    main()