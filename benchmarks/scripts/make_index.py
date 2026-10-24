# -*- coding: utf-8 -*-
"""Generate export/index.html: a file manifest page for the published artifact."""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.join(ROOT, "export")
groups = [
 ("deliverables", "공개용 초안", {"README_table_en.md": "kocer README용 리더보드 표 (영문)", "blog_velog_ko.md": "velog 블로그 초안 (한국어)", "discussion_teamuniva_ko.md": "TeamUNIVA HF Discussion 초안", "discussion_buzzasr_en.md": "BuzzASR HF Discussion 초안. Common Voice 추가 전 발송 보류"}),
 ("results", "채점 결과", {"tables2.md": "최종 표: 4단계 CER, 오류 개수 분해, 단계별 순위, 쌍별 부트스트랩", "scores2.json": "위 표의 원자료", "fake_review.tsv": "가짜 오류 100건 검수 (seed 20261024, 판정 포함)", "fake_error_pool.jsonl": "raw>0, kocer=0 전체 풀 (2,067건)", "NOTES.md": "실험 노트: 환경, 디코딩, 함정, kocer 수정", "ref_stats.md": "참조 전사 숫자·영문·부호 비율", "hyp_stats.md": "모델 출력 스타일 비율", "tables.md": "1차 표 (분모 미보정, 참고용)", "scores.json": "1차 원자료 (참고용)", "common_ids.json": "채점에 쓴 공통 샘플 id"}),
 ("scripts", "스크립트", {}),
 ("kocer_patch", "kocer 패치", {"kocer_0.1.2_patch.diff": "counters.py 주 양쪽 읽기, numbers.py 고유어 단독형, tests 8건 (미커밋)"}),
]
def size(p):
    b = os.path.getsize(p)
    return f"{b/1024:.0f} KB" if b < 1024 * 1024 else f"{b/1024/1024:.1f} MB"
rows = []
for d, title, desc in groups:
    lis = []
    for f in sorted(os.listdir(os.path.join(root, d))):
        p = os.path.join(root, d, f)
        if os.path.isdir(p):
            inner = " · ".join(f'<a href="{d}/{f}/{s}">{html.escape(s)}</a> <span class="sz">{size(os.path.join(p, s))}</span>' for s in sorted(os.listdir(p)))
            lis.append(f'<li><span class="name">{html.escape(f)}/</span><span class="desc">{inner}</span></li>')
        else:
            lis.append(f'<li><a href="{d}/{f}">{html.escape(f)}</a> <span class="sz">{size(p)}</span><span class="desc">{html.escape(desc.get(f, ""))}</span></li>')
    rows.append(f'<section><h2>{html.escape(title)} <span class="path">{d}/</span></h2><ul>{"".join(lis)}</ul></section>')
zip_size = size(os.path.join(root, "kocer_bench_export.zip"))
local_path = "C:" + chr(92) + "Users" + chr(92) + "admin" + chr(92) + "kocer_bench" + chr(92) + "kocer_bench_export.zip"
page = """<title>kocer 리더보드 재채점 파일</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* layout: single-column file manifest grouped by folder */
:root { --bg:#f7f5f0; --fg:#1f1d1a; --muted:#6b655c; --line:#d9d3c7; --accent:#8a3b12; --chip:#ece6da;
  --sans:"IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif; --mono:"IBM Plex Mono", Consolas, monospace; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#1b1917; --fg:#ece7de; --muted:#a39b8e; --line:#3a352f; --accent:#e58b58; --chip:#2a2622; color-scheme: dark } }
:root[data-theme="dark"] { --bg:#1b1917; --fg:#ece7de; --muted:#a39b8e; --line:#3a352f; --accent:#e58b58; --chip:#2a2622; color-scheme: dark }
body { background:var(--bg); color:var(--fg); font-family:var(--sans); font-size:15px; line-height:1.55;
  padding-block:32px 64px; padding-left:max(16px, env(safe-area-inset-left,0px)); padding-right:max(16px, env(safe-area-inset-right,0px)); }
main { max-width:860px; margin:0 auto; }
h1 { font-size:1.6rem; font-weight:600; margin:0 0 .25rem; text-wrap:balance; }
.lead { color:var(--muted); margin:0 0 1.5rem; max-width:65ch; }
.zip { display:flex; flex-wrap:wrap; gap:8px 20px; align-items:baseline; border:1px solid var(--line); padding:14px 16px; margin-bottom:2rem; }
.zip a { font-weight:600; }
h2 { font-size:1.05rem; font-weight:600; margin:2rem 0 .5rem; display:flex; gap:10px; align-items:baseline; }
.path { font-family:var(--mono); font-size:.8rem; color:var(--muted); font-weight:400; }
ul { list-style:none; margin:0; padding:0; border-top:1px solid var(--line); }
li { display:grid; grid-template-columns:minmax(0,1fr) auto; gap:4px 16px; padding:9px 0; border-bottom:1px solid var(--line); min-width:0; }
li .desc { grid-column:1 / -1; color:var(--muted); font-size:.9rem; overflow-wrap:anywhere; }
a { color:var(--accent); text-decoration:none; font-family:var(--mono); font-size:.92rem; overflow-wrap:anywhere; }
a:hover, a:focus-visible { text-decoration:underline; outline:none; }
.name { font-family:var(--mono); font-size:.92rem; }
.sz { font-family:var(--mono); font-size:.8rem; color:var(--muted); font-variant-numeric:tabular-nums; }
.note { background:var(--chip); padding:10px 14px; font-size:.9rem; margin-top:2rem; max-width:65ch; }
</style>
<main>
<h1>kocer 리더보드 재채점 파일</h1>
<p class="lead">2026-10-24 실험 산출물. Zeroth·FLEURS 테스트셋, 6개 모델 설정, 4단계 정규화 채점. 데이터셋 wav와 venv는 포함하지 않음.</p>
<div class="zip"><span class="name">kocer_bench_export.zip</span> <span class="sz">__ZIP__, 51개 파일 전체. 이 페이지에는 압축 파일을 올릴 수 없어 아래 개별 파일로 제공합니다.</span><span class="sz">로컬 사본: __LOCAL__</span></div>
__ROWS__
<p class="note">fake_review.tsv의 판정은 1차(AI 어시스턴트)이며 저자 재확인 전입니다. discussion_buzzasr_en.md는 Common Voice ko를 추가하기 전에는 보내지 않습니다.</p>
</main>"""
page = page.replace("__ZIP__", zip_size).replace("__LOCAL__", local_path).replace("__ROWS__", "".join(rows))
open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(page)
print("index written", len(page))
