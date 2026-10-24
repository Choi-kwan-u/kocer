"""kocer ref.txt hyp.txt [--diff]  — 줄 단위 쌍을 채점."""
import argparse
import sys

from . import __version__, breakdown, measure

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
    p.add_argument("hyp")
    p.add_argument("--diff", action="store_true", help="틀린 글자를 색으로 표시 (빨강=치환/삭제, 초록=삽입)")
    p.add_argument("--no-numbers", action="store_true", help="숫자 정규화 끔")
    p.add_argument("--version", action="version", version=__version__)
    a = p.parse_args(argv)
    refs = open(a.ref, encoding="utf-8").read().splitlines()
    hyps = open(a.hyp, encoding="utf-8").read().splitlines()
    if len(refs) != len(hyps):
        sys.exit(f"줄 수가 다릅니다: ref {len(refs)}, hyp {len(hyps)}")
    if a.diff:
        for i, (r, h) in enumerate(zip(refs, hyps), 1):
            m = measure(r, h, numbers=not a.no_numbers)
            if m.errors:
                print(f"{i}: {render(m.alignment)}  (cer {m.cer:.3f})")
    print(breakdown(refs, hyps, numbers=not a.no_numbers))
    return 0


if __name__ == "__main__":
    sys.exit(main())
