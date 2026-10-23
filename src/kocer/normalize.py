"""단계별 정규화. 각 단계는 독립 함수, normalize()가 순서대로 적용."""
import re
import unicodedata

# 숫자 사이의 . 과 , (3.5 / 1,000)는 남긴다
_PUNCT = re.compile(r"(?<!\d)[.,]|[.,](?!\d)|[?!~…·'\"‘’“”()\[\]{}<>:;/\\_\-—–、。，！？「」『』【】]")
_THOUSANDS = re.compile(r"(?<=\d),(?=\d)")
_FILLER = re.compile(r"(?<!\S)(?:음+|어+|아+|에+|그+)(?!\S)")
_LETTERS = dict(zip(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "에이 비 시 디 이 에프 지 에이치 아이 제이 케이 엘 엠 엔 오 피 큐 알 에스 티 유 브이 더블유 엑스 와이 지".split(),
))
_UNITS = {"%": "퍼센트", "km": "킬로미터", "kg": "킬로그램", "cm": "센티미터", "mm": "밀리미터", "ml": "밀리리터"}
_UNIT_RE = re.compile(r"(?<=\d)\s*(" + "|".join(map(re.escape, sorted(_UNITS, key=len, reverse=True))) + r")(?![A-Za-z])")
# 단어처럼 읽는 약어. 철자 읽기(에이아이)가 기본이고 이건 추가 후보다.
# 일부러 20개 안쪽으로 둔다. 도메인 약어는 사용자가 aliases로 넘긴다.
ALIASES = {
    "NASA": "나사", "UNESCO": "유네스코", "NATO": "나토", "FIFA": "피파", "OPEC": "오펙",
    "AIDS": "에이즈", "COVID": "코비드", "UNICEF": "유니세프", "ASEAN": "아세안", "SARS": "사스",
    "MERS": "메르스", "KOSPI": "코스피", "KOSDAQ": "코스닥", "NASDAQ": "나스닥", "RAM": "램", "LAN": "랜",
}


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def strip_punct(text: str) -> str:
    return _PUNCT.sub(" ", _THOUSANDS.sub("", text))


def strip_fillers(text: str) -> str:
    return _FILLER.sub(" ", text)


def units(text: str) -> str:
    """50% → 50퍼센트, 3km → 3킬로미터. 숫자 바로 뒤의 단위 기호만 바꾼다."""
    return _UNIT_RE.sub(lambda m: _UNITS[m.group(1)], text)


def spell(token: str) -> str:
    """대문자 약어의 철자 읽기. AI → 에이아이."""
    return "".join(_LETTERS[c] for c in token)


def squeeze(text: str) -> str:
    return " ".join(text.split())


def normalize(text: str, punct: bool = True, fillers: bool = False, letters: bool = True) -> str:
    text = nfc(text)
    if punct:
        text = strip_punct(text)
    if fillers:
        text = strip_fillers(text)
    if letters:
        text = units(text)  # 영문 토큰 자체는 numbers.best에서 후보로 전개
    return squeeze(text)
