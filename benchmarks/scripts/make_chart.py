"""results/scores2.json → docs/breakdown{,-en}-{light,dark}.svg : raw 오류를 종류별로 나눈 100% 누적 가로 막대 (한국어·영어)."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, "results", "scores2.json"), encoding="utf-8"))["scores"]
NAMES = {"buzzasr-korean": "BuzzASR/korean", "qwen3-asr-1.7b-ko-univa-release": "TeamUNIVA ko", "qwen3-asr-1.7b-ko-univa": "TeamUNIVA ko beta", "whisper-large-v3": "whisper-large-v3",
         "qwen3-asr-1.7b": "Qwen3-ASR-1.7B", "sensevoice-small-itn": "SenseVoice (itn on)", "sensevoice-small-noitn": "SenseVoice (itn off)"}
rows = []
for tag, name in NAMES.items():
    E = S[tag]["overall"]["E"]
    rows.append((name, [E[0] - E[1], E[1] - E[2], E[2] - E[3], E[3]], S[tag]["overall"]["cer"]))
rows.sort(key=lambda r: r[2]["kocer"])
TEXT = {
    "": dict(title="CER이 센 오류의 절반 가까이는 모델이 틀린 게 아니라 적는 방식 차이입니다",
             sub="공개 한국어 STT 모델 7개 설정, 테스트 1,418발화. 막대 전체가 기존 CER(jiwer)이 센 오류이고, kocer는 노란 부분만 셉니다.",
             legend=["띄어쓰기 차이", "문장부호 차이", "숫자·영문 표기 차이", "진짜 오류 (kocer CER)"], legend_w=11,
             left="← 표기만 다름: kocer는 오류로 안 셈 →", right="← 진짜 오류 →", col="기존 CER → kocer"),
    "-en": dict(title="Up to two thirds of Korean ASR \"errors\" are notation, not recognition",
                sub="7 public Korean ASR settings, 1,418 test utterances. Each bar is everything plain CER (jiwer) counts; kocer counts only the yellow part.",
                legend=["spacing", "punctuation", "number / Latin notation", "real errors (kocer CER)"], legend_w=6.5,
                left="← notation only: not counted by kocer →", right="← real errors →", col="plain CER → kocer"),
}
THEMES = {"light": dict(bg="#fcfcfb", fg="#0b0b0b", muted="#52514e", series=["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]),
          "dark": dict(bg="#1a1a19", fg="#f0efec", muted="#c3c2b7", series=["#3987e5", "#d95926", "#199e70", "#c98500"])}
W, LABEL, RIGHT, BAR, GAP, TOP = 760, 150, 120, 22, 12, 108
for (lang, T), (mode, t) in ((lt, mt) for lt in TEXT.items() for mt in THEMES.items()):
    H = TOP + len(rows) * (BAR + GAP) + 16
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Apple SD Gothic Neo,Malgun Gothic,Noto Sans KR,Segoe UI,Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
         f'<text x="16" y="26" font-size="15" font-weight="600" fill="{t["fg"]}">{T["title"]}</text>',
         f'<text x="16" y="46" font-size="12" fill="{t["muted"]}">{T["sub"]}</text>']
    x = 16
    for c, lab in zip(t["series"], T["legend"]):
        o.append(f'<rect x="{x}" y="56" width="10" height="10" rx="2" fill="{c}"/><text x="{x + 15}" y="65" font-size="11" fill="{t["muted"]}">{lab}</text>')
        x += 15 + T["legend_w"] * len(lab) + 22
    span = W - LABEL - RIGHT
    # 막대 위 안내: 왼쪽 ~60%는 표기 차이, 오른쪽은 진짜 오류 (합산 평균 기준 위치)
    cut = LABEL + span * 0.60
    o.append(f'<text x="{(LABEL + cut) / 2:.0f}" y="{TOP - 12}" font-size="11" text-anchor="middle" fill="{t["muted"]}">{T["left"]}</text>')
    o.append(f'<text x="{(cut + LABEL + span) / 2:.0f}" y="{TOP - 12}" font-size="11" text-anchor="middle" fill="{t["fg"]}">{T["right"]}</text>')
    o.append(f'<text x="{LABEL + span + 10}" y="{TOP - 12}" font-size="11" fill="{t["muted"]}">{T["col"]}</text>')
    for i, (name, parts, cer) in enumerate(rows):
        y = TOP + i * (BAR + GAP); total = sum(parts); x = LABEL
        o.append(f'<text x="{LABEL - 10}" y="{y + 15}" font-size="12" text-anchor="end" fill="{t["fg"]}">{name}</text>')
        for c, v in zip(t["series"], parts):
            w = span * v / total - 2
            o.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w, 0):.1f}" height="{BAR}" rx="2" fill="{c}"/>')
            if v / total >= 0.04:
                o.append(f'<text x="{x + w / 2:.1f}" y="{y + 15}" font-size="11" text-anchor="middle" fill="#0b0b0b">{v / total:.0%}</text>')
            x += span * v / total
        o.append(f'<text x="{LABEL + span + 10}" y="{y + 15}" font-size="11" fill="{t["muted"]}">{cer["raw"]:.2%} → {cer["kocer"]:.2%}</text>')
    o.append("</svg>")
    out = os.path.join(os.path.dirname(ROOT), "docs", f"breakdown{lang}-{mode}.svg")
    open(out, "w", encoding="utf-8").write("\n".join(o)); print(out)
