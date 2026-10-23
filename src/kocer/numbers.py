"""숫자 읽기와 후보 전개."""
from __future__ import annotations

import re
from itertools import product
from typing import Callable, List, Sequence, Tuple

from .counters import lookup

NUMBER = re.compile(r"\d+(?:\.\d+)?")  # 천 단위 콤마는 normalize 단계에서 이미 제거됨

_DIGIT = "영일이삼사오육칠팔구"
_SMALL = ["", "십", "백", "천"]
_BIG = ["", "만", "억", "조", "경"]
_NATIVE_TENS = ["", "열", "스물", "서른", "마흔", "쉰", "예순", "일흔", "여든", "아흔"]
_NATIVE_ONES = ["", "한", "두", "세", "네", "다섯", "여섯", "일곱", "여덟", "아홉"]


def digitwise(s: str) -> str:
    """010 → 공일공, 1234 → 일이삼사 (전화번호·코드)."""
    return "".join("공" if c == "0" else _DIGIT[int(c)] for c in s if c.isdigit())


def _sino_small(n: int) -> str:
    out = []
    for pos in (3, 2, 1, 0):
        d = n // 10**pos % 10
        if d == 0:
            continue
        out.append(("" if d == 1 and pos else _DIGIT[d]) + _SMALL[pos])
    return "".join(out)


def sino(s: str) -> str:
    """한자어 읽기. 2024 → 이천이십사, 15000 → 만오천, 3.5 → 삼점오."""
    if "." in s:
        whole, frac = s.split(".", 1)
        return sino(whole) + "점" + digitwise(frac)
    if s.startswith("0") and len(s) > 1:
        return digitwise(s)
    n = int(s)
    if n == 0:
        return "영"
    parts = []
    i = 0
    while n:
        g, n = n % 10000, n // 10000
        if g:
            parts.append(("" if g == 1 and i == 1 else _sino_small(g)) + _BIG[i])
        i += 1
    return "".join(reversed(parts))


def native(s: str):
    """고유어 관형형 읽기 (3 → 세, 20 → 스무, 21 → 스물한). 1~99만 지원, 그 외 None."""
    if not s.isdigit() or not 1 <= int(s) <= 99:
        return None
    n = int(s)
    if n == 20:
        return "스무"
    return _NATIVE_TENS[n // 10] + _NATIVE_ONES[n % 10]


def options(num: str, following: str) -> List[str]:
    """숫자 하나의 읽기 후보. 원문 숫자는 항상 포함."""
    kind = lookup(following.lstrip())
    opts = [num]
    nat = native(num) if kind != "sino" else None
    if nat:
        opts.append(nat)
    if kind != "native" or not nat:  # 고유어 읽기가 없는 수(100개 → 백 개)는 한자어로
        opts.append(sino(num))
    if len(num) >= 2 and num.isdigit() and not num.startswith("0"):
        opts.append(digitwise(num))  # 2024 → 이공이사, 전화번호 등
    return list(dict.fromkeys(opts))


def _spans(text: str) -> List[Tuple[int, int, List[str]]]:
    return [(m.start(), m.end(), options(m.group(), text[m.end():m.end() + 6])) for m in NUMBER.finditer(text)]


def _build(text: str, spans, choice: Sequence[str]) -> str:
    for (start, end, _), rep in sorted(zip(spans, choice), reverse=True):
        text = text[:start] + rep + text[end:]
    return text


def best(text: str, score: Callable[[str], float], limit: int = 64) -> str:
    """text의 숫자들을 읽기 후보로 바꿔 본 문자열 중 score가 최소인 것."""
    spans = _spans(text)
    if not spans:
        return text
    total = 1
    for _, _, o in spans:
        total *= len(o)
    if total <= limit:
        return min((_build(text, spans, c) for c in product(*(o for _, _, o in spans))), key=score)
    # shortcut: 후보 조합이 limit 초과면 구간별로 따로 고름(다른 구간은 원문 숫자 유지), 인접 구간 간섭으로 틀리면 묶음 전개로 올릴 것
    base = [o[0] for _, _, o in spans]
    choice = []
    for i, (_, _, o) in enumerate(spans):
        choice.append(min(o, key=lambda opt: score(_build(text, spans, base[:i] + [opt] + base[i + 1:]))))
    return _build(text, spans, choice)
