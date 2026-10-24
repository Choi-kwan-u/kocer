"""kocer ref.txt hyp.txt [--diff] [--aihub]  — 줄 단위 쌍을 채점.
kocer ref.txt a.txt b.txt ...  — 결과 파일이 둘 이상이면 모델 비교 (CER, 순위 범위, 쌍별 95% 신뢰구간)."""
import argparse
import sys

import os

from . import __version__, breakdown, compare, measure

RED, GREEN, STRIKE, END = "\x1b[31m", "\x1b[32m", "\x1b[9;31m", "\x1b[0m"


def render(alignment) -> str:
    out = []
    for op, r, h in alignment:
        if op == "H":
            out.append(r)
        elif op == "S":
            out.append(f"{RED}{h}{END}")
        elif op == "D":
            out.append(f"{STRIKE}{r}{END}")
        else:
            out.append(f"{GREEN}{h}{END}")
    return "".join(out)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="kocer", description=__doc__)
    p.add_argument("ref")
    p.add_argument("hyp", nargs="+", help="결과 파일. 둘 이상이면 비교 모드")
    p.add_argument("--diff", action="store_true", help="틀린 글자를 색으로 표시 (빨강=치환/삭제, 초록=삽입)")
    p.add_argument("--no-numbers", action="store_true", help="숫자 정규화 끔")
    p.add_argument("--aihub", action="store_true", help="AI-Hub 전사의 잡음 태그(b/ n/ ...), 간투사 슬래시, +, * 표시를 지움")
    p.add_argument("--no-dual", action="store_true", help="이중 표기 (3시)/(세 시)를 후보로 풀지 않음")
    p.add_argument("--boot", type=int, default=2000, help="비교 모드의 bootstrap 반복 수 (기본 2000)")
    p.add_argument("--version", action="version", version=__version__)
    a = p.parse_args(argv)
    refs = open(a.ref, encoding="utf-8").read().splitlines()
    opts = dict(numbers=not a.no_numbers, aihub=a.aihub, dual=not a.no_dual)
    if len(a.hyp) > 1:
        systems = {}
        for path in a.hyp:
            lines = open(path, encoding="utf-8").read().splitlines()
            if len(lines) != len(refs):
                sys.exit(f"줄 수가 다릅니다: ref {len(refs)}, {path} {len(lines)}")
            name = os.path.splitext(os.path.basename(path))[0]
            systems[name if name not in systems else path] = lines
        print(compare(refs, systems, n_boot=a.boot, **opts))
        return 0
    hyps = open(a.hyp[0], encoding="utf-8").read().splitlines()
    if len(refs) != len(hyps):
        sys.exit(f"줄 수가 다릅니다: ref {len(refs)}, hyp {len(hyps)}")
    if a.diff:
        for i, (r, h) in enumerate(zip(refs, hyps), 1):
            m = measure(r, h, **opts)
            if m.errors:
                print(f"{i}: {render(m.alignment)}  (cer {m.cer:.3f})")
    print(breakdown(refs, hyps, **opts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
