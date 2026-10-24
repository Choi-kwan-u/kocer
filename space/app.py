"""kocer 데모: 정답과 STT 출력을 붙여넣으면 기존 CER, kocer CER, 오류 분해, 틀린 글자를 보여준다."""
import html

import gradio as gr
import kocer

MAX_LINES, MAX_CHARS = 200, 20000  # 무료 CPU에서 한 번에 처리할 양
SEG = [("띄어쓰기", "spacing", "#2a78d6"), ("문장부호", "punctuation", "#eb6834"),
       ("숫자·영문 표기", "numbers_letters", "#1baf7a"), ("진짜 오류", "remaining", "#eda100")]

EXAMPLES = [
    ["사과 세 개 주세요\n세 시 삼십 분에 만나요\n네, 알겠습니다.\n오늘날씨가좋다\n회의는 내일 열립니다",
     "사과 3개 주세요\n3시 30분에 만나요\n네 알겠습니다\n오늘 날씨가 좋다\n회의는 내일 열림니다"],
    ["이천이십사 년 십이 월 이십오 일\n에이아이 모델을 써요\n오천 원입니다",
     "2024년 12월 25일\nAI 모델을 써요.\n5,000원 입니다"],
    ["사과 세 개 주세요\n세 시 삼십 분\n회의는 내일 열립니다",
     "사과 네 개 주세요\n3시 13분\n회의는 내일 열림니다"],
]


def _diff(alignment) -> str:
    out = []
    for op, r, h in alignment:
        if op == "H":
            out.append(html.escape(r))
        elif op == "S":
            out.append(f'<span class="k-sub" title="정답: {html.escape(r)}">{html.escape(h)}</span>')
        elif op == "D":
            out.append(f'<span class="k-del" title="빠진 글자">{html.escape(r)}</span>')
        else:
            out.append(f'<span class="k-ins" title="끼어든 글자">{html.escape(h)}</span>')
    return "".join(out)


def score(ref_text: str, hyp_text: str) -> str:
    refs, hyps = ref_text.strip("\n").split("\n"), hyp_text.strip("\n").split("\n")
    if not ref_text.strip() or not hyp_text.strip():
        return '<p class="k-note">정답과 STT 출력을 한 줄에 한 문장씩 넣어 주세요.</p>'
    if len(refs) != len(hyps):
        return f'<p class="k-note">줄 수가 다릅니다. 정답 {len(refs)}줄, STT 출력 {len(hyps)}줄. 같은 줄끼리 비교합니다.</p>'
    if len(refs) > MAX_LINES or len(ref_text) + len(hyp_text) > MAX_CHARS:
        return f'<p class="k-note">데모는 {MAX_LINES}줄, {MAX_CHARS:,}자까지만 받습니다. 더 큰 데이터는 <code>pip install kocer</code>로 직접 돌려 주세요.</p>'

    b = kocer.breakdown(refs, hyps)
    d = max(b.raw_errors, 1)
    bar = "".join(
        f'<div class="k-seg" style="flex:{getattr(b, key)};background:{c}" title="{name} {getattr(b, key)}개">'
        f'{getattr(b, key) / d:.0%}</div>'
        for name, key, c in SEG if getattr(b, key) > 0)
    legend = "".join(
        f'<span class="k-leg"><i style="background:{c}"></i>{name} <b>{getattr(b, key)}</b>개</span>'
        for name, key, c in SEG)
    rows = []
    for r, h in zip(refs, hyps):
        m = kocer.measure(r, h)
        rows.append(f"<tr><td>{html.escape(r)}</td><td>{html.escape(h)}</td>"
                    f"<td class='k-num'>{m.raw_cer:.1%}</td><td class='k-num'><b>{m.cer:.1%}</b></td>"
                    f"<td>{_diff(m.alignment) if m.errors else '<span class=k-ok>오류 없음</span>'}</td></tr>")
    return f"""
<div class="k-head">
  <div><div class="k-label">기존 CER (jiwer와 같음)</div><div class="k-big">{b.cer['raw']:.1%}</div></div>
  <div class="k-arrow">→</div>
  <div><div class="k-label">kocer CER</div><div class="k-big k-accent">{b.cer['kocer']:.1%}</div></div>
</div>
<p class="k-sub-head">기존 CER이 센 오류 {b.raw_errors}개 중 <b>{(b.raw_errors - b.remaining) / d:.0%}</b>는 모델이 틀린 게 아니라 적는 방식 차이입니다. kocer는 노란 부분만 셉니다.</p>
<div class="k-bar">{bar}</div>
<div class="k-legend">{legend}</div>
<table class="k-table"><thead><tr><th>정답</th><th>STT 출력</th><th>기존</th><th>kocer</th><th>kocer가 센 오류</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<p class="k-note">빨강: 잘못 들은 글자(마우스를 올리면 정답) · 취소선: 빠진 글자 · 초록: 끼어든 글자. 숫자·영문은 kocer가 고른 읽기로 보여줍니다. 한 문장의 kocer CER이 기존보다 높게 나올 수 있는데, 분모(정답 글자 수)에서 공백이 빠지기 때문입니다. 틀린 글자 수는 늘지 않습니다. kocer {kocer.__version__}</p>
"""


CSS = """
.k-head{display:flex;align-items:center;gap:20px;margin:4px 0 8px}
.k-label{font-size:13px;opacity:.75}
.k-big{font-size:34px;font-weight:700;font-variant-numeric:tabular-nums}
.k-accent{color:#c98500}
.k-arrow{font-size:26px;opacity:.6}
.k-sub-head{margin:6px 0 10px}
.k-bar{display:flex;gap:2px;height:28px;border-radius:4px;overflow:hidden}
.k-seg{display:flex;align-items:center;justify-content:center;color:#0b0b0b;font-size:12px;min-width:2px;white-space:nowrap;overflow:hidden}
.k-legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin:8px 0 16px;font-size:13px}
.k-leg i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:baseline}
.k-table{width:100%;border-collapse:collapse;font-size:14px}
.k-table th,.k-table td{border-bottom:1px solid rgba(127,127,127,.25);padding:6px 8px;text-align:left;vertical-align:top}
.k-num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.k-sub{background:rgba(227,73,72,.25);border-bottom:2px solid #e34948}
.k-del{text-decoration:line-through;text-decoration-color:#e34948;opacity:.7}
.k-ins{background:rgba(27,175,122,.25);border-bottom:2px solid #1baf7a}
.k-ok{opacity:.6}
.k-note{font-size:13px;opacity:.75}
"""

with gr.Blocks(title="kocer: 한국어 STT 공정 채점", css=CSS) as demo:
    gr.Markdown(
        "# kocer: 한국어 STT를 공정하게 채점하는 CER\n"
        "띄어쓰기·문장부호·숫자 표기(3개 = 세 개)·영문 약어(AI = 에이아이) 차이는 오류로 세지 않습니다. "
        "정답과 STT 출력을 **한 줄에 한 문장씩** 넣으면 기존 CER과 kocer CER, 오류가 어디서 왔는지 보여줍니다. "
        "입력은 저장하지 않습니다. · [GitHub](https://github.com/Choi-kwan-u/kocer) · `pip install kocer`")
    with gr.Row():
        ref = gr.Textbox(label="정답 (한 줄에 한 문장)", lines=8, value=EXAMPLES[0][0])
        hyp = gr.Textbox(label="STT 출력 (같은 순서)", lines=8, value=EXAMPLES[0][1])
    btn = gr.Button("채점", variant="primary")
    out = gr.HTML(score(*EXAMPLES[0]))  # 들어오자마자 결과가 보이게
    gr.Examples(EXAMPLES, inputs=[ref, hyp], label="예시 (누르면 채워짐)")
    btn.click(score, [ref, hyp], out)
    ref.submit(score, [ref, hyp], out)

if __name__ == "__main__":
    demo.launch()
