"""kocer 데모 (Gradio 버전). 서버 CPU가 있는 Space용. 화면 로직은 demo_core.py."""
import gradio as gr

from demo_core import CSS, EXAMPLES, score

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
