# Sequential candidate choice vs joint optimum (kocer 0.5.0, issue #3)

Joint optimum = minimum error count over every reference-candidate x hypothesis-candidate combination, checked when there are at most 20,000 combinations. Seven settings, every scored pair (KsponSpeech and telephone: both references).

| set | scored pairs | with a choice to make | checked | too many combinations | kocer above optimum | extra errors (total / max per sentence) | corpus CER overstated by (largest setting) |
|---|---|---|---|---|---|---|---|
| zeroth | 3,199 | 535 | 535 | 0 | 0 | 0 / 0 | 0.000 pt |
| fleurs | 2,674 | 909 | 883 | 26 | 1 | 1 / 1 | 0.006 pt |
| commonvoice | 4,053 | 61 | 61 | 0 | 0 | 0 / 0 | 0.000 pt |
| kspon_clean (spelling) | 21,000 | 1,781 | 1,774 | 7 | 6 | 11 / 2 | 0.004 pt |
| kspon_clean (pronunciation) | 21,000 | 1,218 | 1,212 | 6 | 0 | 0 / 0 | 0.000 pt |
| kspon_other (spelling) | 21,000 | 3,148 | 3,109 | 39 | 11 | 25 / 4 | 0.007 pt |
| kspon_other (pronunciation) | 21,000 | 2,059 | 2,058 | 1 | 0 | 0 / 0 | 0.000 pt |
| tel_hr (spelling) | 13,552 | 4,261 | 3,969 | 292 | 2 | 4 / 2 | 0.007 pt |
| tel_hr (pronunciation) | 13,552 | 3,603 | 3,602 | 1 | 0 | 0 / 0 | 0.000 pt |
| **all** | 121,030 | 17,575 | 17,203 | 372 | 20 | 41 / 4 | |
