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
