"""kocer — 한국어 STT를 공정하게 채점하는 CER/WER.
띄어쓰기·문장부호·숫자 표기·영문 약어 차이를 오류로 세지 않는다."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence, Union

from . import numbers as _numbers
from .align import Op, align, distance
from .normalize import normalize as _normalize

__version__ = "0.1.1"
__all__ = ["cer", "wer", "measure", "Result"]

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
            numbers: bool = True, punct: bool = True, fillers: bool = False, letters: bool = True) -> Result:
    raw_ref, raw_hyp = (reference.split(), hypothesis.split()) if unit == "word" else (list(reference), list(hypothesis))
    raw = distance(raw_ref, raw_hyp) / max(len(raw_ref), 1)

    ref, hyp = reference, hypothesis
    if normalize:
        ref = _normalize(reference, punct, fillers, letters)
        hyp = _normalize(hypothesis, punct, fillers, letters)
        if numbers:
            # shortcut: hyp 후보를 먼저 ref 원문에 맞춰 고르고, 그다음 ref 후보를 고른 hyp에 맞춤(양쪽 곱집합 아님), 혼합 표기에서 틀리면 곱집합으로 올릴 것
            hyp = _numbers.best(hyp, lambda c: distance(_units(ref, unit), _units(c, unit)))
            ref = _numbers.best(ref, lambda c: distance(_units(c, unit), _units(hyp, unit)))
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
