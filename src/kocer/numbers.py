"""숫자·영문·단위 토큰의 읽기 후보 전개. 후보 중 CER이 최소인 조합을 고른다.
후보는 '같은 것을 다르게 적은 것'만 넣는다. 빈 문자열처럼 글자를 그냥 없애는 후보는 넣지 않는다 (1만 → 만의 '1'만 예외)."""
from __future__ import annotations

import re
from itertools import product
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from .counters import known, lookup
from .normalize import spell_variants

NUMBER = re.compile(r"\d+(?:\.\d+)?")  # 천 단위 콤마는 normalize 단계에서 이미 제거됨
LATIN = re.compile(r"[A-Za-z]+")
_TIME = re.compile(r"(?<![\d.])(\d+):(\d+)(?![\d.])")              # 3:30 시각, 3:1 비율
_CURRENCY = re.compile(r"([$₩€£¥])\s*(\d+(?:\.\d+)?)")              # $100
_TEMP = re.compile(r"(\d+(?:\.\d+)?)\s*(℃|°C|°)(?![A-Za-z])")        # 25℃ (NFKC 뒤에는 °C)
_NEG = re.compile(r"(?<!\S)-(?=\d)")                                 # -5도. 하이픈(A-1, 010-1234)은 normalize가 이미 지움
_ALNUM = re.compile(r"(?<![A-Za-z\d])(?:([A-Za-z]+)(\d+)|(\d+)([A-Za-z]+))(?![A-Za-z\d])")  # C4, 5G, MP3
# 숫자 뒤 단위 기호. 소문자만: 5G는 단위가 아니라 영문+숫자
UNITS: Dict[str, List[str]] = {"%": ["퍼센트", "프로"], "km": ["킬로미터", "킬로", "키로"], "kg": ["킬로그램", "킬로", "키로"],
                               "cm": ["센티미터", "센티"], "mm": ["밀리미터", "밀리"], "ml": ["밀리리터"], "m": ["미터"], "g": ["그램"]}
_UNIT = re.compile(r"(?<=\d)\s*(?:(km|kg|cm|mm|ml|m|g)(?![A-Za-z])|(%))")
_UNIT_AT_START = re.compile(r"^\s*(?:(km|kg|cm|mm|ml|m|g)(?![A-Za-z])|(%))")
_CURRENCY_WORD = {"$": "달러", "₩": "원", "€": "유로", "£": "파운드", "¥": "엔"}
_ENGLISH_DIGIT = {"0": ["제로", "오"], "1": ["원"], "2": ["투"], "3": ["쓰리"], "4": ["포"], "5": ["파이브"],
                  "6": ["식스"], "7": ["세븐"], "8": ["에잇", "에이트"], "9": ["나인"]}
_BIG_WORDS = ("천", "만", "억", "조")

_DIGIT = "영일이삼사오육칠팔구"
_SMALL = ["", "십", "백", "천"]
_BIG = ["", "만", "억", "조", "경"]
_NATIVE_TENS = ["", "열", "스물", "서른", "마흔", "쉰", "예순", "일흔", "여든", "아흔"]
_NATIVE_ONES = ["", "한", "두", "세", "네", "다섯", "여섯", "일곱", "여덟", "아홉"]
_NATIVE_ONES_ALONE = ["", "하나", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉"]


def digitwise(s: str, zero: str = "공") -> str:
    """010 → 공일공, 1234 → 일이삼사 (전화번호·코드). 0은 공 또는 영(zero="영")."""
    return "".join(zero if c == "0" else _DIGIT[int(c)] for c in s if c.isdigit())


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


def native_forms(s: str) -> List[str]:
    """고유어 읽기 후보 전부: 관형형(세, 스무, 스물한)과 단독형(셋, 스물, 스물하나).
    '스물 센티미터'처럼 조수사 앞에서도 단독형으로 읽는 화자가 있어 둘 다 허용한다."""
    pre = native(s)
    if pre is None:
        return []
    n = int(s)
    return list(dict.fromkeys([pre, _NATIVE_TENS[n // 10] + _NATIVE_ONES_ALONE[n % 10]]))


def options(num: str, following: str) -> List[str]:
    """숫자 하나의 읽기 후보. 원문 숫자는 항상 포함.
    - 조수사 사전에 따라 고유어/한자어. 고유어 조수사라도 20 이상이면 한자어도 (삼십오 명).
    - 6월·10월은 유월·시월, 1번째는 첫 번째, 0 단독은 공/영, 1만·1천은 만·천.
    - 자릿수 읽기(34 → 삼사)는 0으로 시작하거나 4자리 이상이거나 조수사가 안 붙을 때만: '삼 사 일'(3~4일)과 '34일'은 다른 말이다."""
    following = following.lstrip()
    following = _UNIT_AT_START.sub(lambda m: UNITS[m.group(1) or m.group(2)][0], following)  # 단위 기호는 읽기로 바꿔 조수사 판단
    kind = lookup(following)
    opts = [num]
    nat = native_forms(num) if kind != "sino" else []
    opts.extend(nat)
    big = num.isdigit() and int(num) >= 20
    if kind != "native" or not nat or big:  # 고유어 읽기가 없는 수(100개 → 백 개)와 20 이상은 한자어로도
        if following.startswith("월") and num in ("6", "10"):
            opts.append({"6": "유", "10": "시"}[num])
        else:
            opts.append(sino(num))
    if num == "1":
        if following.startswith("번째") or following.startswith("째"):
            opts.append("첫")
        if following[:1] in _BIG_WORDS:
            opts.append("")  # 1만 원 = 만 원 = 일만 원
    if num == "0":
        opts.append("공")
    if num.isdigit() and len(num) >= 2:
        if num.startswith("0"):
            opts.append(digitwise(num, "영"))  # 010 → 공일공(위 sino)과 영일영
        elif len(num) >= 4 or not known(following):
            opts += [digitwise(num), digitwise(num, "영")]  # 2024 → 이공이사·이영이사, 전화번호 등
    return list(dict.fromkeys(opts))


def _hour_forms(h: str) -> List[str]:
    forms = [h]
    nat = native(h)
    if nat:
        forms.append(nat)
    forms.append(sino(h))
    return list(dict.fromkeys(forms))


def time_or_ratio_options(a: str, b: str) -> List[str]:
    """3:30 → 세 시 삼십 분 (0~23 : 00~59, 분은 두 자리). 그 밖의 a:b → 삼 대 일."""
    orig = f"{a}:{b}"
    if len(b) == 2 and int(a) <= 23 and int(b) <= 59:
        mi = int(b)
        mins = list(dict.fromkeys([str(mi), sino(str(mi))])) if mi else []
        out = [orig]
        for hf in _hour_forms(a):
            if not mi:
                out.append(f"{hf}시")
            out += [f"{hf}시 {mf}분" for mf in mins]
        return out
    return [orig] + [f"{x} 대 {y}" for x in dict.fromkeys([a, sino(a)]) for y in dict.fromkeys([b, sino(b)])]


def currency_options(sym: str, num: str) -> List[str]:
    word = _CURRENCY_WORD[sym]
    return [sym + num] + [f"{r} {word}" for r in dict.fromkeys([num, sino(num)])]


def temperature_options(num: str, sym: str) -> List[str]:
    out = [num + sym]
    for r in dict.fromkeys([num, sino(num)]):
        out += [f"{r}도", f"섭씨 {r}도"]
    return out


def unit_options(sym: str) -> List[str]:
    return [sym] + UNITS[sym]


def alnum_options(letters: str, digits: str, letters_first: bool, aliases: Dict[str, str]) -> List[str]:
    """C4 → 씨포, 5G → 오지/파이브지. 영문에 붙은 숫자에만 영어 읽기를 연다 (모든 숫자에 열면 후보가 폭발하고 오탐이 는다)."""
    l_opts = latin_options(letters, aliases)
    d_opts = [digits, sino(digits)] + (_ENGLISH_DIGIT[digits] if len(digits) == 1 else [])
    pairs = product(l_opts, d_opts) if letters_first else product(d_opts, l_opts)
    out = ["".join(p) for p in pairs]
    return list(dict.fromkeys(out))[:12]


def latin_options(token: str, aliases: Dict[str, str]) -> List[str]:
    """영문 토큰의 후보: 철자 읽기(대소문자 무관), 사전에 있으면 사전 읽기, 원문."""
    opts = spell_variants(token)
    alias = aliases.get(token) or aliases.get(token.upper())
    if alias:
        opts.append(alias)
    opts += [token, token.upper()]  # 대문자 원문도 후보: ai = AI
    return list(dict.fromkeys(opts))


def _spans(text: str, digits: bool, aliases: Optional[Dict[str, str]]) -> List[Tuple[int, int, List[str]]]:
    """(start, end, 후보들). 앞선 규칙이 먼저 자리를 잡고, 겹치는 뒤 규칙은 버린다 (3:30은 시각이지 3과 30이 아님)."""
    found: List[Tuple[int, int, List[str]]] = []

    def add(start: int, end: int, opts: List[str]):
        if len(opts) > 1 and not any(start < e and s < end for s, e, _ in found):
            found.append((start, end, opts))

    letters = aliases is not None
    if digits:
        for m in _TIME.finditer(text):
            add(m.start(), m.end(), time_or_ratio_options(m.group(1), m.group(2)))
        for m in _CURRENCY.finditer(text):
            add(m.start(), m.end(), currency_options(m.group(1), m.group(2)))
        for m in _TEMP.finditer(text):
            add(m.start(), m.end(), temperature_options(m.group(1), m.group(2)))
        for m in _NEG.finditer(text):
            add(m.start(), m.end(), ["-", "마이너스", "영하"])
    if letters:
        for m in _UNIT.finditer(text):
            add(m.start(), m.end(), unit_options(m.group(1) or m.group(2)))
    if digits and letters:
        for m in _ALNUM.finditer(text):
            if m.group(1) is not None:
                add(m.start(), m.end(), alnum_options(m.group(1), m.group(2), True, aliases))
            else:
                add(m.start(), m.end(), alnum_options(m.group(4), m.group(3), False, aliases))
    if digits:
        for m in NUMBER.finditer(text):
            add(m.start(), m.end(), options(m.group(), text[m.end():m.end() + 6]))
    if letters:
        for m in LATIN.finditer(text):
            add(m.start(), m.end(), latin_options(m.group(), aliases))
    return sorted(found)


def _build(text: str, spans, choice: Sequence[str]) -> str:
    for (start, end, _), rep in sorted(zip(spans, choice), reverse=True):
        text = text[:start] + rep + text[end:]
    return text


def best(text: str, score: Callable[[str], float], limit: int = 64, digits: bool = True,
         aliases: Optional[Dict[str, str]] = None) -> str:
    """text의 숫자(digits)와 영문·단위 토큰(aliases가 None이 아니면)을 후보로 바꿔 본 문자열 중 score가 최소인 것."""
    spans = _spans(text, digits, aliases)
    if not spans:
        return text
    total = 1
    for _, _, o in spans:
        total *= len(o)
    if total <= limit:
        return min((_build(text, spans, c) for c in product(*(o for _, _, o in spans))), key=score)
    # shortcut: 후보 조합이 limit 초과면 구간별로 따로 고름(다른 구간은 원문 유지), 인접 구간 간섭으로 틀리면 묶음 전개로 올릴 것
    base = [o[0] for _, _, o in spans]
    choice = []
    for i, (_, _, o) in enumerate(spans):
        choice.append(min(o, key=lambda opt: score(_build(text, spans, base[:i] + [opt] + base[i + 1:]))))
    return _build(text, spans, choice)
