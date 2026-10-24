"""kocer — 한국어 STT를 공정하게 채점하는 CER/WER.
띄어쓰기·문장부호·숫자 표기·영문 약어 차이를 오류로 세지 않는다."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Union

from . import numbers as _numbers
from .align import Op, align, distance
from .normalize import ALIASES
from .normalize import DUAL as _DUAL
from .normalize import dual_variants as _dual_variants
from .normalize import normalize as _normalize
from .normalize import resolve_dual as _resolve_dual
from .normalize import strip_aihub_tags as _strip_aihub

__version__ = "0.3.0"
__all__ = ["cer", "wer", "measure", "breakdown", "compare", "Result", "Breakdown", "Comparison", "ALIASES"]

Text = Union[str, Sequence[str]]


@dataclass
class Result:
    cer: float            # 정규화 후 오류율 (unit="word"면 WER)
    raw_cer: float        # 정규화 전 오류율 (jiwer와 같은 값)
    hits: int
    substitutions: int
    deletions: int
    insertions: int
    alignment: List[Op] = field(repr=False)
    chosen_ref: str = ""  # 숫자 후보 중 실제로 채택된 정답
    chosen_hyp: str = ""

    @property
    def ops(self):
        return {"S": self.substitutions, "D": self.deletions, "I": self.insertions}

    @property
    def errors(self) -> int:
        return self.substitutions + self.deletions + self.insertions


def _units(text: str, unit: str) -> List[str]:
    return text.split() if unit == "word" else list(text.replace(" ", ""))


def _normalized(ref: str, hyp: str, unit: str, numbers: bool, punct: bool, fillers: bool, letters: bool,
                aliases: Optional[Dict[str, str]]):
    """정규화 + 숫자·영문 후보 선택 후의 (ref, hyp, alignment)."""
    ref = _normalize(ref, punct, fillers, letters)
    hyp = _normalize(hyp, punct, fillers, letters)
    table = {**ALIASES, **(aliases or {})} if letters else None
    if numbers or letters:
        # shortcut: hyp 후보를 먼저 ref 원문에 맞춰 고르고, 그다음 ref 후보를 고른 hyp에 맞춤(양쪽 곱집합 아님), 혼합 표기에서 틀리면 곱집합으로 올릴 것
        hyp = _numbers.best(hyp, lambda c: distance(_units(ref, unit), _units(c, unit)), digits=numbers, aliases=table)
        ref = _numbers.best(ref, lambda c: distance(_units(c, unit), _units(hyp, unit)), digits=numbers, aliases=table)
    return ref, hyp, align(_units(ref, unit), _units(hyp, unit))


def _pick(cands):
    """(ref, hyp, ops) 후보 중 오류가 가장 적은 것. 같으면 정답이 긴 쪽(숫자·영문 후보와 같은 규칙)."""
    def key(c):
        ops = c[2]
        return (sum(op != "H" for op, _, _ in ops), -sum(op != "I" for op, _, _ in ops))
    return min(cands, key=key)


def _dual_sides(text: str):
    """이중 표기 구간 수."""
    return len(_DUAL.findall(text))


def measure(reference: str, hypothesis: str, *, unit: str = "char", normalize: bool = True,
            numbers: bool = True, punct: bool = True, fillers: bool = False, letters: bool = True,
            aliases: Optional[Dict[str, str]] = None, dual: bool = True, aihub: bool = False) -> Result:
    """aliases: 단어처럼 읽는 약어 사전 (예: {"NASA": "나사"}). 내장 ALIASES 위에 덮어쓴다.
    dual: AI-Hub 이중 표기 "(3시)/(세 시)"의 양쪽을 모두 정답 후보로 본다 (기본 켬).
    aihub: AI-Hub 전사의 잡음 태그(b/ n/ ...), 간투사 슬래시, 반복(+)·불명확(*) 표시를 지운다 (기본 끔)."""
    raw_ref, raw_hyp = (reference.split(), hypothesis.split()) if unit == "word" else (list(reference), list(hypothesis))
    raw = distance(raw_ref, raw_hyp) / max(len(raw_ref), 1)

    if not normalize:
        ops = align(raw_ref, raw_hyp)
        ref, hyp = reference, hypothesis
    else:
        ref_text, hyp_text = reference, hypothesis
        if aihub:
            ref_text, hyp_text = _strip_aihub(ref_text), _strip_aihub(hyp_text)
        args = (unit, numbers, punct, fillers, letters, aliases)
        if dual and (_DUAL.search(ref_text) or _DUAL.search(hyp_text)):
            refs, hyps = _dual_variants(ref_text), _dual_variants(hyp_text)
            if refs is not None and hyps is not None and len(refs) * len(hyps) <= 16:
                ref, hyp, ops = _pick([_normalized(r, h, *args) for r in refs for h in hyps])
            else:
                # shortcut: 구간이 많으면 구간별로 철자/발음을 하나씩 고름(다른 구간은 현재 선택 유지), 정답·결과 양쪽에 이중 표기가 많으면 틀릴 수 있음
                def greedy(text, other, as_ref):
                    sides = [1] * _dual_sides(text)
                    for i in range(len(sides)):
                        best_side = None
                        for s in (1, 2):
                            trial = sides[:i] + [s] + sides[i + 1:]
                            t = _resolve_dual(text, trial)
                            c = _normalized(t, other, *args) if as_ref else _normalized(other, t, *args)
                            if best_side is None or _pick([best_side[1], c]) is c:
                                best_side = (s, c)
                        sides[i] = best_side[0]
                    return _resolve_dual(text, sides)
                hyp_text = greedy(hyp_text, _DUAL.sub(r"\1", ref_text), as_ref=False) if _DUAL.search(hyp_text) else hyp_text
                ref_text = greedy(ref_text, hyp_text, as_ref=True) if _DUAL.search(ref_text) else ref_text
                ref, hyp, ops = _normalized(ref_text, hyp_text, *args)
        else:
            ref, hyp, ops = _normalized(ref_text, hyp_text, *args)
    counts = {k: sum(op == k for op, _, _ in ops) for k in "HSDI"}
    err = counts["S"] + counts["D"] + counts["I"]
    n = counts["H"] + counts["S"] + counts["D"]
    return Result(err / max(n, 1), raw, counts["H"], counts["S"], counts["D"], counts["I"], ops, ref, hyp)


def _rate(reference: Text, hypothesis: Text, unit: str, **opts) -> float:
    if isinstance(reference, str):
        reference, hypothesis = [reference], [hypothesis]
    if len(reference) != len(hypothesis):
        raise ValueError("reference and hypothesis must have the same length")
    results = [measure(r, h, unit=unit, **opts) for r, h in zip(reference, hypothesis)]
    total = sum(x.hits + x.substitutions + x.deletions for x in results)
    return sum(x.errors for x in results) / max(total, 1)


def cer(reference: Text, hypothesis: Text, **opts) -> float:
    """jiwer.cer 호환. 문자열 하나 또는 리스트."""
    return _rate(reference, hypothesis, "char", **opts)


def wer(reference: Text, hypothesis: Text, **opts) -> float:
    """jiwer.wer 호환. 띄어쓰기 차이는 오류로 센다 (한국어 WER의 한계)."""
    return _rate(reference, hypothesis, "word", **opts)


@dataclass
class Breakdown:
    """raw CER가 센 오류를 띄어쓰기 / 문장부호 / 숫자·영문 표기 / 진짜 오류로 나눈 개수."""
    pairs: int
    raw_errors: int
    spacing: int
    punctuation: int
    numbers_letters: int
    remaining: int
    cer: Dict[str, float]  # 단계별 CER: raw, nospace, nopunct, kocer

    @property
    def shares(self) -> Dict[str, float]:
        d = max(self.raw_errors, 1)
        return {"spacing": self.spacing / d, "punctuation": self.punctuation / d,
                "numbers_letters": self.numbers_letters / d, "remaining": self.remaining / d}

    def __str__(self) -> str:
        rows = [("띄어쓰기", self.spacing), ("문장부호", self.punctuation), ("숫자·영문", self.numbers_letters), ("진짜 오류", self.remaining)]
        d = max(self.raw_errors, 1)
        out = [f"raw CER {self.cer['raw']:.2%}  →  kocer CER {self.cer['kocer']:.2%}   ({self.raw_errors:,} raw errors, {self.pairs:,} pairs, kocer {__version__})"]
        out += [f"{name:<6}{n:>8,}  {n / d:4.0%}  {'█' * round(40 * n / d)}" for name, n in rows]
        return "\n".join(out)


def breakdown(reference: Text, hypothesis: Text, **opts) -> Breakdown:
    """raw → 공백 제거 → 공백·부호 제거 → kocer 네 단계로 채점해 오류가 어디서 사라지는지 개수로 센다.
    각 단계는 정답과 결과에 똑같이 적용된다. opts는 cer()와 같다(aliases 등)."""
    if isinstance(reference, str):
        reference, hypothesis = [reference], [hypothesis]
    if len(reference) != len(hypothesis):
        raise ValueError("reference and hypothesis must have the same length")
    # 이중 표기 해소는 숫자·영문 칸(같은 말의 다른 표기), AI-Hub 태그 제거는 문장부호 칸으로 들어가게 단계별로 켠다
    levels = [dict(normalize=False), dict(numbers=False, punct=False, letters=False, dual=False, aihub=False),
              dict(numbers=False, letters=False, dual=False), {}]
    E, N = [0] * 4, [0] * 4
    for r, h in zip(reference, hypothesis):
        for i, lv in enumerate(levels):
            m = measure(r, h, **{**opts, **lv}) if lv else measure(r, h, **opts)
            E[i] += m.errors
            N[i] += m.hits + m.substitutions + m.deletions
    cer = dict(zip(("raw", "nospace", "nopunct", "kocer"), (e / max(n, 1) for e, n in zip(E, N))))
    return Breakdown(len(reference), E[0], E[0] - E[1], E[1] - E[2], E[2] - E[3], E[3], cer)


from .compare import Comparison, compare  # noqa: E402  (measure를 쓰므로 맨 아래에서 가져옴)
