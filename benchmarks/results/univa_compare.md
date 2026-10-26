
## CER (%) — raw

| model | zeroth | fleurs | commonvoice | pooled |
|---|---|---|---|---|
| base | 7.60 | 6.08 | 7.32 | 6.97 |
| beta | 9.28 | 6.20 | 7.04 | 7.61 |
| release | 8.89 | 6.25 | 6.85 | 7.43 |

## CER (%) — card (punct+case, spaces kept)

| model | zeroth | fleurs | commonvoice | pooled |
|---|---|---|---|---|
| base | 5.62 | 4.52 | 6.60 | 5.45 |
| beta | 7.00 | 4.60 | 6.27 | 5.96 |
| release | 6.94 | 4.50 | 6.22 | 5.88 |

## CER (%) — card + spaces removed

| model | zeroth | fleurs | commonvoice | pooled |
|---|---|---|---|---|
| base | 3.72 | 4.53 | 6.68 | 4.72 |
| beta | 5.44 | 4.37 | 6.30 | 5.26 |
| release | 5.36 | 4.36 | 6.18 | 5.19 |

## CER (%) — kocer

| model | zeroth | fleurs | commonvoice | pooled |
|---|---|---|---|---|
| base | 2.90 | 4.25 | 6.61 | 4.27 |
| beta | 2.44 | 4.25 | 6.08 | 3.96 |
| release | 2.34 | 4.19 | 6.00 | 3.89 |

## Where raw errors go (pooled counts, share of raw)

| model | raw errors | spacing+punct (card+space level) | numbers/letters (kocer only) | remaining |
|---|---|---|---|---|
| base | 4521 | 2236 (49%) | 215 (5%) | 2070 (46%) |
| beta | 4935 | 2389 (48%) | 626 (13%) | 1920 (39%) |
| release | 4816 | 2302 (48%) | 631 (13%) | 1883 (39%) |

## Number-writing habit: share of hypotheses containing a digit / punctuation

| model | zeroth digit | zeroth punct | fleurs digit | fleurs punct | commonvoice digit | commonvoice punct |
|---|---|---|---|---|---|---|
| base | 8.5% | 99.8% | 19.4% | 100.0% | 0.7% | 99.1% |
| beta | 31.7% | 100.0% | 23.8% | 100.0% | 2.1% | 97.9% |
| release | 31.3% | 99.1% | 25.4% | 99.7% | 1.9% | 95.3% |

## Paired bootstrap, release - beta and release - base (2,000 resamples, seed 0, sentence level)

| comparison | level | zeroth | fleurs | commonvoice | pooled |
|---|---|---|---|---|---|
| release - beta | raw | -0.39 [-0.65,-0.16]* | +0.04 [-0.14,+0.22] | -0.19 [-0.60,+0.22] | -0.18 [-0.34,-0.03]* |
| release - beta | card + spaces removed | -0.08 [-0.25,+0.09] | -0.01 [-0.16,+0.15] | -0.12 [-0.55,+0.30] | -0.07 [-0.20,+0.07] |
| release - beta | kocer | -0.09 [-0.26,+0.06] | -0.06 [-0.19,+0.08] | -0.08 [-0.49,+0.34] | -0.08 [-0.21,+0.05] |
| release - base | raw | +1.29 [+0.77,+1.83]* | +0.16 [-0.11,+0.43] | -0.47 [-0.92,-0.07]* | +0.46 [+0.21,+0.70]* |
| release - base | card + spaces removed | +1.64 [+1.11,+2.21]* | -0.17 [-0.45,+0.09] | -0.50 [-0.97,-0.03]* | +0.47 [+0.21,+0.76]* |
| release - base | kocer | -0.56 [-0.82,-0.31]* | -0.05 [-0.28,+0.18] | -0.61 [-1.06,-0.14]* | -0.39 [-0.55,-0.22]* |
