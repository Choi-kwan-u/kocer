"""단계별 정규화. 각 단계는 독립 함수, normalize()가 순서대로 적용.
숫자·영문·단위 기호는 여기서 바꾸지 않고 numbers.py가 후보로 전개한다."""
import re
import unicodedata
from itertools import product
from typing import List

# 남기는 부호: 숫자 사이의 . , : (3.5 / 1,000 / 3:30), 공백·문장 시작 뒤 숫자 바로 앞의 - (-5도). 나머지는 공백으로.
_PUNCT = re.compile(r"(?<!\d)[.,:]|[.,:](?!\d)|(?<=\S)-|-(?!\d)"
                    r"|[?!~…·'\"‘’“”()\[\]{}<>;/\\_—–、。，！？「」『』【】]")
_THOUSANDS = re.compile(r"(?<=\d),(?=\d)")
_FILLER = re.compile(r"(?<!\S)(?:음+|어+|아+|에+|그+)(?!\S)")
# 폭 없는 문자·BOM·소프트 하이픈. 메모장 BOM(﻿)과 복사해 온 ​가 흔하다.
_ZERO_WIDTH = re.compile(r"[﻿​‌‍⁠­]")
_LETTERS = dict(zip(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "에이 비 시 디 이 에프 지 에이치 아이 제이 케이 엘 엠 엔 오 피 큐 알 에스 티 유 브이 더블유 엑스 와이 지".split(),
))
# 두 가지로 읽는 글자만. 첫 번째가 기본 읽기.
_LETTER_VARIANTS = {"C": ["시", "씨"], "Z": ["지", "제트"], "R": ["알", "아르"]}
# 단어처럼 읽는 약어. 철자 읽기(에이아이)가 기본이고 이건 추가 후보다.
# 일부러 20개 안쪽으로 둔다. 도메인 약어는 사용자가 aliases로 넘긴다.
ALIASES = {
    "NASA": "나사", "UNESCO": "유네스코", "NATO": "나토", "FIFA": "피파", "OPEC": "오펙",
    "AIDS": "에이즈", "COVID": "코비드", "UNICEF": "유니세프", "ASEAN": "아세안", "SARS": "사스",
    "MERS": "메르스", "KOSPI": "코스피", "KOSDAQ": "코스닥", "NASDAQ": "나스닥", "RAM": "램", "LAN": "랜",
}


# AI-Hub(ETRI) 전사 규칙. 이중 표기 "(철자)/(발음)" 예: "(3시)/(세 시)"
DUAL = re.compile(r"\(([^()]*)\)/\(([^()]*)\)")
# 잡음 태그 b/ l/ o/ n/ u/ (앞이 영문자가 아닌 소문자 하나 + 슬래시), 간투사 표시 "어/", 반복 "+", 불명확 "*"
_AIHUB_TAG = re.compile(r"(?<![A-Za-z])[a-z]/")
_AIHUB_FILLER_SLASH = re.compile(r"(?<=[가-힣])/(?=[\s.,?!]|$)")
_AIHUB_MARKS = re.compile(r"[+*]")
# 다른 AI-Hub 데이터의 잡음·이벤트 태그: (NO:) (SN:) (SP:) (FP:), /(noise), @웃음. 이중 표기 "(A)/(B)"의 "/(B)"는 건드리지 않는다.
_AIHUB_PAREN_TAG = re.compile(r"\([A-Z]{2}:\)")
_AIHUB_SLASH_PAREN = re.compile(r"(?<!\))/\([^()/]*\)")
_AIHUB_EVENT = re.compile(r"@(?:웃음|기침|박수|한숨|노래|잡음|숨소리|울음|재채기|하품|헛기침)")


def strip_aihub_tags(text: str) -> str:
    """AI-Hub 전사의 잡음 태그·간투사 슬래시·반복(+)·불명확(*) 표시를 지운다. 이중 표기 (A)/(B)는 건드리지 않는다.
    가림 태그(@이름1, &이름&)는 지우지 않는다: 지우면 모델이 받아쓴 실제 이름이 전부 삽입 오류가 된다."""
    text = _AIHUB_PAREN_TAG.sub(" ", text)
    text = _AIHUB_SLASH_PAREN.sub(" ", text)
    text = _AIHUB_EVENT.sub(" ", text)
    text = _AIHUB_TAG.sub(" ", text)
    text = _AIHUB_FILLER_SLASH.sub("", text)
    return squeeze(_AIHUB_MARKS.sub("", text))


def dual_variants(text: str, limit: int = 16):
    """이중 표기 (A)/(B)를 풀어 만든 후보 문자열들. 구간이 많아 조합이 limit를 넘으면 None (호출 쪽에서 구간별 선택)."""
    spans = list(DUAL.finditer(text))
    if not spans:
        return [text]
    if 2 ** len(spans) > limit:
        return None
    out = []
    for mask in range(2 ** len(spans)):
        pieces, last = [], 0
        for i, m in enumerate(spans):
            pieces += [text[last:m.start()], m.group(2 if mask >> i & 1 else 1)]
            last = m.end()
        out.append("".join(pieces) + text[last:])
    return out


def resolve_dual(text: str, sides) -> str:
    """구간마다 고른 쪽(1=철자, 2=발음)으로 이중 표기를 푼다."""
    it = iter(sides)
    return DUAL.sub(lambda m: m.group(next(it)), text)


def nfkc(text: str) -> str:
    """NFKC: 전각 ＡＩ → AI, ㎞ → km, ℃ → °C, 자모 분리 입력 → 완성형. 폭 없는 문자는 지운다. 수학 마이너스(−)는 하이픈으로."""
    return unicodedata.normalize("NFKC", _ZERO_WIDTH.sub("", text)).replace("−", "-")


nfc = nfkc  # 0.3 이전 이름


def strip_punct(text: str) -> str:
    return _PUNCT.sub(" ", _THOUSANDS.sub("", text))


def strip_fillers(text: str) -> str:
    return _FILLER.sub(" ", text)


def spell(token: str) -> str:
    """대문자 약어의 기본 철자 읽기. AI → 에이아이."""
    return "".join(_LETTERS[c] for c in token.upper() if c in _LETTERS)


def spell_variants(token: str, limit: int = 4) -> List[str]:
    """철자 읽기 후보. 두 가지로 읽는 글자(C 시/씨, Z 지/제트, R 알/아르)를 조합하되 limit개까지. 첫 항목이 기본 읽기."""
    choices = [_LETTER_VARIANTS.get(c, [_LETTERS[c]]) for c in token.upper() if c in _LETTERS]
    out = []
    for combo in product(*choices):
        out.append("".join(combo))
        if len(out) >= limit:
            break
    return out


def squeeze(text: str) -> str:
    return " ".join(text.split())


_FRACTION_SLASH = re.compile(r"(?<![\d/])(\d{1,3})/(\d{1,3})(?![\d/])")
_KEEP = ""  # placeholder for a fraction slash while punctuation is stripped


def normalize(text: str, punct: bool = True, fillers: bool = False, fractions: bool = False) -> str:
    """fractions=True keeps the slash of a simple a/b (1/2, 3/4) so the number step can read it as 이분의 일.
    Without it the slash is punctuation, as before."""
    text = nfkc(text)
    if punct:
        if fractions:
            text = _FRACTION_SLASH.sub(lambda m: m.group(1) + _KEEP + m.group(2), text)
        text = strip_punct(text).replace(_KEEP, "/")
    if fillers:
        text = strip_fillers(text)
    return squeeze(text)
