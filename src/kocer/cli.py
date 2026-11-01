"""kocer ref.txt hyp.txt [--diff] [--aihub] [--style digits]  : 줄 단위 쌍을 채점.
kocer ref.txt a.txt b.txt ...  : 결과 파일이 둘 이상이면 모델 비교 (CER, 순위 범위, 쌍별 95% 신뢰구간).
kocer keywords ref.txt hyp.txt --list kw.txt  : 키워드 오류율 (kw.txt는 줄마다 키워드 하나)."""
import argparse
import sys

import os

from . import __version__, breakdown, compare, keywords, measure

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


def _read(path):
    return open(path, encoding="utf-8-sig").read().splitlines()


def _common(p):
    p.add_argument("--no-numbers", action="store_true", help="숫자 정규화 끔")
    p.add_argument("--aihub", action="store_true", help="AI-Hub 전사의 잡음 태그(b/ n/ ...), 간투사 슬래시, +, * 표시를 지움")
    p.add_argument("--no-dual", action="store_true", help="이중 표기 (3시)/(세 시)를 후보로 풀지 않음")


def _keywords_main(argv) -> int:
    p = argparse.ArgumentParser(prog="kocer keywords", description="키워드 오류율: 키워드가 정답에 나온 횟수와 결과에서 맞은 횟수")
    p.add_argument("ref")
    p.add_argument("hyp", nargs="+", help="결과 파일. 여러 개면 각각 출력")
    p.add_argument("--list", required=True, metavar="FILE", help="줄마다 키워드 하나")
    _common(p)
    a = p.parse_args(argv)
    refs = _read(a.ref)
    words = [w.strip() for w in _read(a.list) if w.strip()]
    opts = dict(numbers=not a.no_numbers, aihub=a.aihub, dual=not a.no_dual)
    for path in a.hyp:
        hyps = _read(path)
        if len(refs) != len(hyps):
            sys.exit(f"줄 수가 다릅니다: ref {len(refs)}, {path} {len(hyps)}")
        if len(a.hyp) > 1:
            print(os.path.splitext(os.path.basename(path))[0])
        print(keywords(refs, hyps, words, **opts))
    return 0


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv[:1] == ["keywords"]:
        return _keywords_main(argv[1:])
    p = argparse.ArgumentParser(prog="kocer", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ref")
    p.add_argument("hyp", nargs="+", help="결과 파일. 둘 이상이면 비교 모드")
    p.add_argument("--diff", action="store_true", help="틀린 글자를 색으로 표시 (빨강=치환/삭제, 초록=삽입)")
    _common(p)
    p.add_argument("--boot", type=int, default=2000, help="비교 모드의 bootstrap 반복 수 (기본 2000)")
    p.add_argument("--style", choices=("digits", "hangul"), help="결과가 이 표기로 수를 썼는지 따로 셈 (점수는 그대로)")
    p.add_argument("--version", action="version", version=__version__)
    a = p.parse_args(argv)
    refs = _read(a.ref)
    opts = dict(numbers=not a.no_numbers, aihub=a.aihub, dual=not a.no_dual)
    if len(a.hyp) > 1:
        systems = {}
        for path in a.hyp:
            lines = _read(path)
            if len(lines) != len(refs):
                sys.exit(f"줄 수가 다릅니다: ref {len(refs)}, {path} {len(lines)}")
            name = os.path.splitext(os.path.basename(path))[0]
            systems[name if name not in systems else path] = lines
        print(compare(refs, systems, n_boot=a.boot, **opts))
        if a.style:
            for name, lines in systems.items():
                b = breakdown(refs, lines, style=a.style, **opts)
                print(f"{name}: 표기 위반 ({a.style}) {b.notation:,}자, 인식 오류 + 표기 위반 CER {b.cer['service']:.2%}")
        return 0
    hyps = _read(a.hyp[0])
    if len(refs) != len(hyps):
        sys.exit(f"줄 수가 다릅니다: ref {len(refs)}, hyp {len(hyps)}")
    if a.diff:
        for i, (r, h) in enumerate(zip(refs, hyps), 1):
            m = measure(r, h, **opts)
            if m.errors:
                print(f"{i}: {render(m.alignment)}  (cer {m.cer:.3f})")
    print(breakdown(refs, hyps, style=a.style, **opts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
