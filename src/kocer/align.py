"""편집거리 + 정렬. 문자 리스트든 단어 리스트든 같은 코드.
rapidfuzz가 있으면 정렬도 rapidfuzz로 한다(전체 행렬을 만들지 않아 긴 입력에서 빠르고 메모리가 적다).
편집거리가 같은 정렬이 여럿이면 둘이 다른 경로를 고를 수 있다: 오류 총수와 CER은 같고, S/D/I 내역만 다를 수 있다."""
from typing import List, Sequence, Tuple

Op = Tuple[str, str, str]  # ('H'|'S'|'D'|'I', ref_item, hyp_item)


def _align_py(ref: Sequence[str], hyp: Sequence[str]) -> List[Op]:
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


def _align_rf(ref: Sequence[str], hyp: Sequence[str]) -> List[Op]:
    ops: List[Op] = []
    for tag, i1, i2, j1, j2 in _opcodes(ref, hyp):
        if tag == "equal":
            ops += [("H", ref[i1 + k], hyp[j1 + k]) for k in range(i2 - i1)]
            continue
        k = min(i2 - i1, j2 - j1) if tag == "replace" else 0
        ops += [("S", ref[i1 + x], hyp[j1 + x]) for x in range(k)]
        ops += [("D", ref[i], "") for i in range(i1 + k, i2)]
        ops += [("I", "", hyp[j]) for j in range(j1 + k, j2)]
    return ops


def distance(ref: Sequence[str], hyp: Sequence[str]) -> int:
    return sum(op != "H" for op, _, _ in _align_py(ref, hyp))


align = _align_py
try:  # pip install "kocer[fast]" — 후보 채점이 수십 배 빨라지고 긴 입력도 빠르다. 없으면 위 순수 파이썬으로.
    from rapidfuzz.distance.Levenshtein import distance  # noqa: F811
    from rapidfuzz.distance.Levenshtein import opcodes as _opcodes
    align = _align_rf
except ImportError:
    pass
