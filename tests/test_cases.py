import csv
import pathlib
import unicodedata

import pytest

import kocer
from kocer import numbers

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name("cases.tsv"), encoding="utf-8"), delimiter="\t"))


@pytest.mark.parametrize("row", ROWS, ids=[f"{r['ref']}|{r['hyp']}" for r in ROWS])
def test_golden(row):
    assert kocer.cer(row["ref"], row["hyp"]) == pytest.approx(float(row["cer"]), abs=1e-4)


def test_raw_cer_is_reported_alongside():
    r = kocer.measure("네, 알겠습니다.", "네 알겠습니다")
    assert r.cer == 0 and r.raw_cer > 0
    assert kocer.cer("네, 알겠습니다.", "네 알겠습니다", normalize=False) == pytest.approx(r.raw_cer)


def test_numbers_can_be_turned_off():
    assert kocer.cer("세 개", "3개", numbers=False) > 0


def test_nfd_input():
    assert kocer.cer(unicodedata.normalize("NFD", "한글 테스트"), "한글 테스트") == 0


def test_list_input_matches_jiwer_style_corpus_rate():
    refs, hyps = ["가나", "다라마"], ["가나", "다라바"]
    assert kocer.cer(refs, hyps) == pytest.approx(1 / 5)


def test_wer_basic():
    assert kocer.wer("오늘 날씨 좋다", "오늘 날씨 좋다") == 0
    assert kocer.wer("오늘 날씨 좋다", "오늘 날씨 춥다") == pytest.approx(1 / 3)


@pytest.mark.parametrize("n,expect", [("0", "영"), ("7", "칠"), ("10", "십"), ("11", "십일"), ("100", "백"),
                                      ("2024", "이천이십사"), ("10000", "만"), ("15000", "만오천"),
                                      ("100000000", "일억"), ("1000000", "백만"), ("3.5", "삼점오"), ("010", "공일공")])
def test_sino(n, expect):
    assert numbers.sino(n) == expect


@pytest.mark.parametrize("n,expect", [("1", "한"), ("3", "세"), ("10", "열"), ("11", "열한"), ("20", "스무"),
                                      ("21", "스물한"), ("99", "아흔아홉"), ("100", None), ("0", None)])
def test_native(n, expect):
    assert numbers.native(n) == expect


def test_many_numbers_fall_back_to_greedy_without_blowing_up():
    ref = " ".join(f"{i}개" for i in range(1, 13))
    hyp = " ".join(["한 개", "두 개", "세 개", "네 개", "다섯 개", "여섯 개", "일곱 개", "여덟 개", "아홉 개", "열 개", "열한 개", "열두 개"])
    assert kocer.cer(ref, hyp) == 0


def test_pure_python_distance_matches_rapidfuzz_when_installed():
    rf = pytest.importorskip("rapidfuzz.distance.Levenshtein")
    from kocer.align import align
    pairs = [("세시삼십분", "3시13분"), ("", "가나"), ("가나다", ""), (list("오늘 날씨".split()), list("오늘 춥다".split()))]
    for a, b in pairs:
        assert sum(op != "H" for op, _, _ in align(a, b)) == rf.distance(a, b)


def test_user_aliases():
    assert kocer.cer("유니스트 입학", "UNIST 입학") > 0
    assert kocer.cer("유니스트 입학", "UNIST 입학", aliases={"UNIST": "유니스트"}) == 0
    assert kocer.cer("애플 주가", "Apple 주가", aliases={"Apple": "애플"}) == 0


def test_letters_off_keeps_latin_as_is():
    assert kocer.cer("에이아이", "AI", letters=False) > 0
    assert kocer.cer("나사", "NASA", letters=False) > 0


def test_builtin_alias_list_stays_small():
    assert len(kocer.ALIASES) <= 20  # 사전 유지보수가 프로젝트를 잡아먹지 않게


def test_breakdown_counts_add_up_and_match_cer():
    refs = ["네, 알겠습니다.", "사과 세 개 주세요", "오늘날씨가좋다", "안녕하세요"]
    hyps = ["네 알겠습니다", "사과 3개 주세요", "오늘 날씨가 좋다", "안녕하세유"]
    b = kocer.breakdown(refs, hyps)
    assert b.pairs == 4
    assert b.spacing + b.punctuation + b.numbers_letters + b.remaining == b.raw_errors
    assert b.punctuation == 2 and b.numbers_letters > 0 and b.remaining == 1
    assert b.cer["kocer"] == pytest.approx(kocer.cer(refs, hyps))
    assert b.cer["raw"] == pytest.approx(kocer.cer(refs, hyps, normalize=False))
    assert abs(sum(b.shares.values()) - 1) < 1e-9
    assert "진짜 오류" in str(b)
