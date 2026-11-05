"""Epoch Merkle tree: pairwise combination with promotion of an unpaired last node.

Level 0 = leaves.  Level l+1 node j = Th(tweak(kid,e,NODE,l+1,j), left||right) for
children 2j, 2j+1 of level l; if level l has an odd count, its last node is
promoted unchanged to level l+1 (it contributes no sibling to any path).
The root is the single node of the top level (for N = 1 the root is the leaf).
Path length for leaf i is between floor(log2 N) and ceil(log2 N).
"""
from .th import Th, tweak, TYPE_LEAF, TYPE_NODE, TYPE_PERIOD


def leaf_hash(kid, epoch, idx, tenant, r, enc_c, n):
    return Th(tweak(kid, epoch, TYPE_LEAF, 0, idx, tenant), r + enc_c, n)


def build_tree(kid, epoch, leaves, n, typ=TYPE_NODE):
    if not leaves:
        raise ValueError("empty tree")
    levels = [list(leaves)]
    cur = levels[0]
    lvl = 0
    while len(cur) > 1:
        lvl += 1
        nxt = []
        m = len(cur)
        for j in range(m // 2):
            nxt.append(Th(tweak(kid, epoch, typ, lvl, j), cur[2 * j] + cur[2 * j + 1], n))
        if m & 1:
            nxt.append(cur[-1])
        levels.append(nxt)
        cur = nxt
    return cur[0], levels


def auth_path(levels, i):
    path = []
    for lv in levels[:-1]:
        sib = i ^ 1
        if sib < len(lv):
            path.append(lv[sib])
        i >>= 1
    return path


def path_len(N, i):
    """Number of siblings on the path of leaf i in a tree of N leaves."""
    d = 0
    m = N
    while m > 1:
        if (i ^ 1) < m:
            d += 1
        i >>= 1
        m = (m + 1) // 2
    return d


def root_from_path(kid, epoch, i, N, leaf, path, n, typ=TYPE_NODE):
    """Recompute the root; returns None if the path has the wrong length or i >= N."""
    if i >= N or i < 0:
        return None
    x = leaf
    m = N
    lvl = 0
    k = 0
    while m > 1:
        lvl += 1
        if (i ^ 1) < m:
            if k >= len(path):
                return None
            sib = path[k]
            k += 1
            if i & 1:
                x = Th(tweak(kid, epoch, typ, lvl, i >> 1), sib + x, n)
            else:
                x = Th(tweak(kid, epoch, typ, lvl, i >> 1), x + sib, n)
        i >>= 1
        m = (m + 1) // 2
    if k != len(path):
        return None
    return x


def period_root(kid, period, epoch_roots, n):
    """Merkle tree hash over the epoch roots of one period (TYPE_PERIOD domain)."""
    leaves = [Th(tweak(kid, period, TYPE_PERIOD, 0, j), r, n) for j, r in enumerate(epoch_roots)]
    root, _ = build_tree(kid, period, leaves, n, typ=TYPE_PERIOD)
    return root


def treehash_paths(kid, epoch, leaf_fn, N, targets, n):
    """Streaming tree hash for N = 2^d leaves with O(d) memory: returns (root, {i: path}) for the
    leaf indices in `targets`.  leaf_fn(i) -> n-byte leaf hash.  Produces the same root/paths as
    build_tree/auth_path (power-of-two N)."""
    assert N & (N - 1) == 0
    d = N.bit_length() - 1
    want = {}  # (level, j) -> list of targets needing that node as sibling
    for i in targets:
        for l in range(d):
            want.setdefault((l, (i >> l) ^ 1), []).append(i)
    paths = {i: [None] * d for i in targets}
    stack = []  # (level, j, hash)
    for i in range(N):
        node = (0, i, leaf_fn(i))
        while True:
            l, j, h = node
            for t in want.get((l, j), ()):
                paths[t][l] = h
            if stack and stack[-1][0] == l:
                _, jl, hl = stack.pop()
                node = (l + 1, j >> 1, Th(tweak(kid, epoch, TYPE_NODE, l + 1, j >> 1), hl + h, n))
            else:
                stack.append(node)
                break
    return stack[0][2], paths
