"""여러 STT 결과를 같은 정답에 대해 비교: 시스템별 CER, 순위와 그 범위, 쌍별 차이의 95% 신뢰구간.
신뢰구간은 문장 단위 paired bootstrap(같은 문장 묶음을 모든 시스템에 함께 다시 뽑음)으로 구한다.
numpy가 있으면 그것으로, 없으면 순수 파이썬으로 계산한다(결과 숫자는 난수 생성기가 달라 조금 다를 수 있다)."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, List, Mapping, Sequence, Tuple


@dataclass
class Comparison:
    cer: Dict[str, float]                                   # 시스템별 코퍼스 CER (총 오류 / 총 정답 글자)
    pairs: Dict[Tuple[str, str], Tuple[float, float, float]]  # (a, b) -> (CER a − CER b, 하한, 상한)
    ranks: Dict[str, Tuple[int, int, float]]                # 시스템 -> (순위 하한, 상한, 1위 확률)
    n: int                                                  # 문장 수
    n_boot: int
    confidence: float
    version: str = field(default="", repr=False)

    def significant(self, a: str, b: str) -> bool:
        """a와 b의 차이가 신뢰구간 기준으로 0이 아닌가."""
        if (a, b) in self.pairs:
            d, lo, hi = self.pairs[(a, b)]
        else:
            d, lo, hi = self.pairs[(b, a)]
            d, lo, hi = -d, -hi, -lo
        return lo > 0 or hi < 0

    def __str__(self) -> str:
        order = sorted(self.cer, key=self.cer.get)
        w = max(len(s) for s in order)
        pct = f"{self.confidence:.0%}"
        out = [f"CER ({self.n:,} pairs, {self.n_boot:,} bootstrap resamples, {pct} intervals, kocer {self.version})"]
        for i, s in enumerate(order, 1):
            lo, hi, p1 = self.ranks[s]
            out.append(f"  {i}. {s:<{w}}  {self.cer[s]:6.2%}   rank range [{lo}, {hi}]   P(1st) {p1:.2f}")
        out.append(f"Pairwise difference (row − col, %p), {pct} interval, * = differs from 0")
        for a, b in combinations(order, 2):
            d, lo, hi = self.pairs[(a, b)]
            mark = " *" if lo > 0 or hi < 0 else ""
            out.append(f"  {a:<{w}} − {b:<{w}}  {d * 100:+.2f}  [{lo * 100:+.2f}, {hi * 100:+.2f}]{mark}")
        return "\n".join(out)


def _quantile(sorted_vals: List[float], q: float) -> float:
    """선형 보간 분위수 (numpy 기본값과 같은 방식)."""
    pos = (len(sorted_vals) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def _bootstrap(E: Dict[str, List[int]], N: Dict[str, List[int]], n: int, n_boot: int, seed: int) -> Dict[str, List[float]]:
    """시스템별 bootstrap CER 표본. 모든 시스템이 같은 재표본 인덱스를 공유한다(paired)."""
    names = list(E)
    try:
        import numpy as np
    except ImportError:
        np = None
    if np is not None:
        rng = np.random.default_rng(seed)
        e = {s: np.asarray(E[s], dtype=np.int64) for s in names}
        m = {s: np.asarray(N[s], dtype=np.int64) for s in names}
        out = {s: [] for s in names}
        chunk = max(1, min(n_boot, 2_000_000 // max(n, 1)))
        done = 0
        while done < n_boot:
            k = min(chunk, n_boot - done)
            idx = rng.integers(0, n, (k, n))
            for s in names:
                out[s].extend((e[s][idx].sum(1) / np.maximum(m[s][idx].sum(1), 1)).tolist())
            done += k
        return out
    rng = random.Random(seed)
    population = range(n)
    out = {s: [] for s in names}
    for _ in range(n_boot):
        idx = rng.choices(population, k=n)
        for s in names:
            es, ns = E[s], N[s]
            out[s].append(sum(es[i] for i in idx) / max(sum(ns[i] for i in idx), 1))
    return out


def compare(references: Sequence[str], systems: Mapping[str, Sequence[str]], *, n_boot: int = 2000,
            seed: int = 0, confidence: float = 0.95, **opts) -> Comparison:
    """references: 정답 문장 리스트. systems: {"이름": 결과 문장 리스트, ...} (2개 이상).
    opts는 cer()와 같다 (normalize=False면 정규화 없는 CER로 비교, aihub=True 등)."""
    from . import __version__, measure
    if isinstance(references, str):
        raise TypeError("references must be a list of sentences")
    if len(systems) < 2:
        raise ValueError("compare needs at least two systems")
    n = len(references)
    for name, hyps in systems.items():
        if len(hyps) != n:
            raise ValueError(f"system {name!r} has {len(hyps)} sentences, references have {n}")
    E: Dict[str, List[int]] = {}
    N: Dict[str, List[int]] = {}
    for name, hyps in systems.items():
        rs = [measure(r, h, **opts) for r, h in zip(references, hyps)]
        E[name] = [x.errors for x in rs]
        N[name] = [x.ref_len for x in rs]
    cer = {s: sum(E[s]) / max(sum(N[s]), 1) for s in systems}
    boot = _bootstrap(E, N, n, n_boot, seed)
    a_lo, a_hi = (1 - confidence) / 2, 1 - (1 - confidence) / 2
    order = sorted(cer, key=cer.get)
    pairs = {}
    for a, b in combinations(order, 2):
        diffs = sorted(x - y for x, y in zip(boot[a], boot[b]))
        pairs[(a, b)] = (cer[a] - cer[b], _quantile(diffs, a_lo), _quantile(diffs, a_hi))
    names = list(systems)
    rank_samples = {s: [] for s in names}
    for j in range(n_boot):
        ordered = sorted(names, key=lambda s: boot[s][j])
        for r, s in enumerate(ordered, 1):
            rank_samples[s].append(r)
    ranks = {}
    for s in names:
        rs = sorted(rank_samples[s])
        ranks[s] = (int(round(_quantile(rs, a_lo))), int(round(_quantile(rs, a_hi))), rs.count(1) / n_boot)
    return Comparison(cer, pairs, ranks, n, n_boot, confidence, __version__)
