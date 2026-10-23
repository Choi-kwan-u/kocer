"""편집거리 + 정렬. 문자 리스트든 단어 리스트든 같은 코드."""
from typing import List, Sequence, Tuple

Op = Tuple[str, str, str]  # ('H'|'S'|'D'|'I', ref_item, hyp_item)


def align(ref: Sequence[str], hyp: Sequence[str]) -> List[Op]:
    n, m = len(ref), len(hyp)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][0] = i
    for j in range(1, m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]))
    ops: List[Op] = []
    i, j = n, m
    while i or j:
        if i and j and d[i][j] == d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]):
            ops.append(("H" if ref[i - 1] == hyp[j - 1] else "S", ref[i - 1], hyp[j - 1]))
            i, j = i - 1, j - 1
        elif i and d[i][j] == d[i - 1][j] + 1:
            ops.append(("D", ref[i - 1], ""))
            i -= 1
        else:
            ops.append(("I", "", hyp[j - 1]))
            j -= 1
    return ops[::-1]


def distance(ref: Sequence[str], hyp: Sequence[str]) -> int:
    return sum(op != "H" for op, _, _ in align(ref, hyp))
