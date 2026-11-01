"""표기 검사 (#6). 결과가 원하는 표기(style)로 숫자를 썼는지 센다. 채점 규칙과는 별개라 점수는 바꾸지 않는다.
- style="digits": 한글 수사로 적힌 수(세 시, 이십오 분, 이천이십사년)가 위반
- style="hangul": 아라비아 숫자(3시, 25분)가 위반
위반 글자 수는 수사 부분만 센다(조수사는 제외). 한글 수사 찾기는 근사다: 조수사·단위 앞의 수사, 자리 단위(십백천만억조)가 든 두 글자 이상의 수,
스물·서른 같은 고유어 십 단위만 잡는다. '이 사람'의 '이'처럼 지시어와 겹치는 한 글자 수사는 띄어 쓰면 세지 않는다."""
import re
from typing import List, Tuple

from .counters import NATIVE, SINO
from .numbers import NUMBER, UNITS

STYLES = ("digits", "hangul")

_SINO = "영공일이삼사오육칠팔구십백천만억조경"
_PLACE = "십백천만억조경"
_NATIVE_TENS = "스물|스무|서른|마흔|예순|일흔|여든|아흔|쉰|열"
_NATIVE_ONES = "다섯|여섯|일곱|여덟|아홉|하나|한|두|둘|세|셋|네|넷"
_NATIVE = rf"(?:(?:{_NATIVE_TENS})(?:{_NATIVE_ONES})?|(?:{_NATIVE_ONES}))"
_SINO_RUN = rf"[{_SINO}]+(?:점[{_SINO}]+)?"
_COUNTERS = sorted((NATIVE | SINO | {"분", "시", "초", "년", "개"} | {w for ws in UNITS.values() for w in ws}), key=len, reverse=True)
_COUNTER = "|".join(map(re.escape, _COUNTERS))
_B = r"(?<![가-힣])"  # 수사 앞에 한글이 붙어 있으면 다른 말의 일부

# 1) 수사 + (공백) + 조수사·단위. 2) 자리 단위가 든 한자어 수 단독. 3) 고유어 십 단위 단독(스물, 서른 ...). 4) 유월·시월, 첫 번째
_HANGUL_NUMBER = re.compile(
    rf"{_B}(?P<n1>{_SINO_RUN}|{_NATIVE})(?P<sp>\s?)(?={_COUNTER})"
    rf"|{_B}(?P<n2>[{_SINO}]*[{_PLACE}][{_SINO}]*(?:점[{_SINO}]+)?)(?![가-힣])"
    rf"|{_B}(?P<n3>(?:{_NATIVE_TENS})(?:{_NATIVE_ONES})?)(?![가-힣])"
    rf"|{_B}(?P<n4>유|시)(?=월)|{_B}(?P<n5>첫)(?=\s?번째)"
)


def hangul_numbers(text: str) -> List[Tuple[int, int]]:
    """한글 수사로 적힌 수의 (start, end). 조수사는 포함하지 않는다."""
    out = []
    for m in _HANGUL_NUMBER.finditer(text):
        g = next(k for k in ("n1", "n2", "n3", "n4", "n5") if m.group(k))
        s, e = m.span(g)
        if g == "n1" and e - s == 1 and m.group("sp") and text[s] in "이그저":
            continue  # '이 사람', '이 시간': 지시어
        if g == "n3" and text[s:e] in ("열", "쉰"):
            continue  # 한 글자 단독은 다른 말과 겹친다 (열이 나다)
        out.append((s, e))
    return out


def digit_numbers(text: str) -> List[Tuple[int, int]]:
    return [m.span() for m in NUMBER.finditer(text)]


def violations(text: str, style: str) -> int:
    """정규화된 결과 문자열에서 style에 어긋나게 적힌 수의 글자 수 (숫자는 자릿수, 한글은 수사 글자 수; 공백·소수점은 빼고)."""
    if style not in STYLES:
        raise ValueError(f"style must be one of {STYLES}")
    spans = hangul_numbers(text) if style == "digits" else digit_numbers(text)
    return sum(sum(c not in " ." for c in text[s:e]) for s, e in spans)
