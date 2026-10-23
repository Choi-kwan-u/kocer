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
_CAPS = re.compile(r"[A-Z]+")


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def strip_punct(text: str) -> str:
    return _PUNCT.sub(" ", _THOUSANDS.sub("", text))


def strip_fillers(text: str) -> str:
    return _FILLER.sub(" ", text)


def spell_letters(text: str) -> str:
    """AI → 에이아이, 50% → 50퍼센트. 대문자 연속과 단위 기호만 바꾼다."""
    text = _UNIT_RE.sub(lambda m: _UNITS[m.group(1)], text)
    return _CAPS.sub(lambda m: "".join(_LETTERS[c] for c in m.group()), text)


def squeeze(text: str) -> str:
    return " ".join(text.split())


def normalize(text: str, punct: bool = True, fillers: bool = False, letters: bool = True) -> str:
    text = nfc(text)
    if punct:
        text = strip_punct(text)
    if fillers:
        text = strip_fillers(text)
    if letters:
        text = spell_letters(text)
    return squeeze(text)
