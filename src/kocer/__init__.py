"""kocer — 한국어 STT를 공정하게 채점하는 CER/WER.
띄어쓰기·문장부호·숫자 표기·영문 약어 차이를 오류로 세지 않는다."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Union

from . import numbers as _numbers
from .align import Op, align, distance
from .normalize import ALIASES
from .normalize import normalize as _normalize

__version__ = "0.1.8"
__all__ = ["cer", "wer", "measure", "breakdown", "Result", "Breakdown", "ALIASES"]

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


def measure(reference: str, hypothesis: str, *, unit: str = "char", normalize: bool = True,
            numbers: bool = True, punct: bool = True, fillers: bool = False, letters: bool = True,
            aliases: Optional[Dict[str, str]] = None) -> Result:
    """aliases: 단어처럼 읽는 약어 사전 (예: {"NASA": "나사"}). 내장 ALIASES 위에 덮어쓴다."""
    raw_ref, raw_hyp = (reference.split(), hypothesis.split()) if unit == "word" else (list(reference), list(hypothesis))
    raw = distance(raw_ref, raw_hyp) / max(len(raw_ref), 1)

    ref, hyp = reference, hypothesis
    if normalize:
        ref = _normalize(reference, punct, fillers, letters)
        hyp = _normalize(hypothesis, punct, fillers, letters)
        table = {**ALIASES, **(aliases or {})} if letters else None
        if numbers or letters:
            # shortcut: hyp 후보를 먼저 ref 원문에 맞춰 고르고, 그다음 ref 후보를 고른 hyp에 맞춤(양쪽 곱집합 아님), 혼합 표기에서 틀리면 곱집합으로 올릴 것
            hyp = _numbers.best(hyp, lambda c: distance(_units(ref, unit), _units(c, unit)), digits=numbers, aliases=table)
            ref = _numbers.best(ref, lambda c: distance(_units(c, unit), _units(hyp, unit)), digits=numbers, aliases=table)
    r, h = (_units(ref, unit), _units(hyp, unit)) if normalize else (raw_ref, raw_hyp)
    ops = align(r, h)
    counts = {k: sum(op == k for op, _, _ in ops) for k in "HSDI"}
    err = counts["S"] + counts["D"] + counts["I"]
    return Result(err / max(len(r), 1), raw, counts["H"], counts["S"], counts["D"], counts["I"], ops, ref, hyp)


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
    levels = [dict(normalize=False), dict(numbers=False, punct=False, letters=False), dict(numbers=False, letters=False), {}]
    E, N = [0] * 4, [0] * 4
    for r, h in zip(reference, hypothesis):
        for i, lv in enumerate(levels):
            m = measure(r, h, **{**opts, **lv}) if lv else measure(r, h, **opts)
            E[i] += m.errors
            N[i] += m.hits + m.substitutions + m.deletions
    cer = dict(zip(("raw", "nospace", "nopunct", "kocer"), (e / max(n, 1) for e, n in zip(E, N))))
    return Breakdown(len(reference), E[0], E[0] - E[1], E[1] - E[2], E[2] - E[3], E[3], cer)
