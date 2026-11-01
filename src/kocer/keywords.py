"""키워드 오류율 (#5). 사용자가 넘긴 키워드(지점명, 상품명, 시각, 금액 ...)가 정답에 나온 횟수와 결과에서 살아남은 횟수를 센다.
키워드 목록은 패키지에 없다. 도메인마다 달라서 사용자가 넘긴다.
판정: kocer 정규화 뒤, 키워드는 공백을 빼고 어절 첫머리에서부터 맞춘다. 어절 안의 공백은 무시하고('서초 점' = '서초점'), 조사는 붙어도 된다('서초점은').
'지점'의 '점'처럼 어절 중간에 섞인 글자는 세지 않는다. 키워드와 문장의 숫자·영문은 읽기 후보로 전개해서 '3시' = '세 시', 'KBO' = '케이비오'."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from . import numbers as _numbers
from .normalize import ALIASES, DUAL
from .normalize import normalize as _normalize
from .normalize import strip_aihub_tags as _strip_aihub

TEXT_LIMIT = 256  # 문장 후보가 이보다 많으면 원문(숫자 그대로)만 본다


@dataclass
class Keywords:
    counts: Dict[str, Tuple[int, int, int]]  # 키워드 -> (정답에 나온 횟수, 결과에서 맞은 횟수, 결과에만 더 나온 횟수)
    pairs: int

    @property
    def total(self) -> int:
        return sum(n for n, _, _ in self.counts.values())

    @property
    def hits(self) -> int:
        return sum(h for _, h, _ in self.counts.values())

    @property
    def rate(self) -> float:
        """키워드 오류율 = 놓친 횟수 / 정답에 나온 횟수."""
        return (self.total - self.hits) / max(self.total, 1)

    def __str__(self) -> str:
        from . import __version__
        w = max([len(k) for k in self.counts] + [4])
        out = [f"keyword error rate {self.rate:.2%}   ({self.total - self.hits} missed of {self.total}, {self.pairs:,} pairs, kocer {__version__})",
               f"{'키워드':<{w}}  정답  맞음  추가"]
        for k, (n, h, x) in self.counts.items():
            out.append(f"{k:<{w}}  {n:>4}  {h:>4}  {x:>4}")
        return "\n".join(out)


def _forms(text: str, numbers: bool, table: Optional[Dict[str, str]], limit: int) -> List[str]:
    """text를 읽기 후보로 바꿔 본 문자열들. 조합이 limit를 넘으면 원문만."""
    c = _numbers.candidates(text, digits=numbers, aliases=table, limit=limit) if (numbers or table is not None) else None
    return list(dict.fromkeys(c or [text]))


def _pattern(forms: Sequence[str]) -> re.Pattern:
    """어절 첫머리에서 시작하고, 키워드 글자 사이의 공백은 무시."""
    alts = sorted({f.replace(" ", "") for f in forms if f.strip()}, key=len, reverse=True)
    return re.compile(r"(?<!\S)(?:" + "|".join(r"\s*".join(map(re.escape, a)) for a in alts) + ")")


def _count(pattern: re.Pattern, forms: Sequence[str]) -> int:
    return max(len(pattern.findall(f)) for f in forms)


def keywords(references: Sequence[str], hypotheses: Sequence[str], words: Sequence[str], *, numbers: bool = True,
             punct: bool = True, fillers: bool = False, letters: bool = True, aliases: Optional[Dict[str, str]] = None,
             dual: bool = True, aihub: bool = False) -> Keywords:
    """words: 키워드 목록. 여러 어절이어도 된다('서초 점' = '서초점'). 한 문장에 같은 키워드가 여러 번 나오면 횟수대로 센다.
    맞음 = 문장마다 min(정답 횟수, 결과 횟수). 옵션은 cer()와 같다."""
    if isinstance(references, str) or isinstance(hypotheses, str) or isinstance(words, str):
        raise TypeError("references, hypotheses and words must be lists")
    if len(references) != len(hypotheses):
        raise ValueError("references and hypotheses must have the same length")
    table = {**ALIASES, **(aliases or {})} if letters else None
    pats = {w: _pattern(_forms(_normalize(w, punct, fillers, fractions=numbers), numbers, table, 4096)) for w in words}
    counts = {w: [0, 0, 0] for w in words}
    for r, h in zip(references, hypotheses):
        if aihub:
            r, h = _strip_aihub(r), _strip_aihub(h)
        rs = [DUAL.sub(r"\1", r), DUAL.sub(r"\2", r)] if dual and DUAL.search(r) else [r]
        hs = [DUAL.sub(r"\1", h), DUAL.sub(r"\2", h)] if dual and DUAL.search(h) else [h]
        rf = [f for x in rs for f in _forms(_normalize(x, punct, fillers, fractions=numbers), numbers, table, TEXT_LIMIT)]
        hf = [f for x in hs for f in _forms(_normalize(x, punct, fillers, fractions=numbers), numbers, table, TEXT_LIMIT)]
        for w, p in pats.items():
            n, m = _count(p, rf), _count(p, hf)
            hit = min(n, m)
            counts[w][0] += n
            counts[w][1] += hit
            counts[w][2] += m - hit
    return Keywords({w: tuple(v) for w, v in counts.items()}, len(references))
