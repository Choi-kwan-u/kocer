"""동결 검사: 기본 설정의 점수가 동결 버전(0.5.1)과 같은지. 저장소의 공개 벤치마크 결과 파일(7 시스템 + 카드 설정, 공개 3 세트) 전 쌍을 다시 채점해
시스템·세트별 (errors, ref_len) 해시를 tests/freeze.json과 비교한다. 점수가 바뀌는 수정은 마이너 버전을 올리고 이 파일을 다시 만든다 (python tests/test_freeze.py)."""
import hashlib
import json
import pathlib

import pytest

import kocer

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / "benchmarks" / "results"
EXPECTED = pathlib.Path(__file__).with_name("freeze.json")


def digests():
    ids = json.loads((RESULTS / "common_ids.json").read_text(encoding="utf-8"))
    out = {}
    for d in sorted(RESULTS.iterdir()):
        if not d.is_dir():
            continue
        for ds in ("zeroth", "fleurs", "commonvoice"):
            f = d / f"{ds}.jsonl"
            if not f.exists():
                continue
            keep = set(ids[ds])
            h = hashlib.sha256()
            for line in f.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                if r["id"] in keep:
                    m = kocer.measure(r["ref"], r["hyp"])
                    h.update(f"{r['id']}\t{m.errors}\t{m.ref_len}\t{m.raw_cer:.6f}\n".encode())
            out[f"{d.name}/{ds}"] = h.hexdigest()
    return out


@pytest.mark.skipif(not RESULTS.exists(), reason="benchmark results are not in this checkout")
def test_default_scores_match_frozen_version():
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    got = digests()
    missing = [k for k in expected["digests"] if k not in got]
    assert not missing, f"result files missing: {missing}"
    # 새 결과 폴더가 추가되는 건 괜찮다 (freeze.json을 다시 만들 때 포함된다)
    changed = [k for k in expected["digests"] if got[k] != expected["digests"][k]]
    assert not changed, f"scores differ from kocer {expected['version']} on: {changed}"


if __name__ == "__main__":
    EXPECTED.write_text(json.dumps({"version": kocer.__version__, "digests": digests()}, indent=1) + "\n", encoding="utf-8")
    print("wrote", EXPECTED, "with kocer", kocer.__version__)
