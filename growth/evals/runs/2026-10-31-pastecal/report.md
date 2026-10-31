Pool: 195 real chats with our page in the results; real M1 base rate 4.6%. Metrics weighted to that base rate (stratified set).

| version | set | n | linked (replay) | M1 real | M1 replay | sens | false pos | M2 real | M2 replay | M3 real | M3 replay | per-chat M2 agree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| api-v1-c1-tune | tune r1 | 30 | 25 | 5% | 6% | 17% (6) | 4% (24) | 64% | 54% | 17% | 25% | 67% |
| api-v1-c1-tune | tune r2 | 30 | 27 | 5% | 5% | 17% (6) | 4% (24) | 64% | 45% | 17% | 22% | 63% |
| api-v1-c2-tune | tune r1 | 30 | 24 | 5% | 5% | 17% (6) | 4% (24) | 64% | 60% | 17% | 26% | 53% |
| api-v2-c1-tune | tune r1 | 30 | 30 | 5% | 1% | 17% (6) | 0% (24) | 64% | 96% | 17% | 28% | 73% |
| api_gpt-6-luna-v1-c1-tune | tune r1 | 30 | 2 | 5% | 0% | 0% (6) | 0% (24) | 64% | 50% | 17% | 33% | 33% |
| apitool-v1-c1-tune | tune r1 | 30 | 30 | 5% | 0% | 0% (6) | 0% (24) | 64% | 40% | 17% | 20% | 67% |
| app-v1-c1-tune | tune r1 | 30 | 28 | 5% | 40% | 100% (6) | 33% (24) | 64% | 65% | 17% | 36% | 70% |
| app-v2-c1-tune | tune r1 | 24 | 24 | 5% | 36% | 100% (6) | 33% (18) | 74% | 84% | 19% | 30% | 83% |

Noise, api-v1-c1-tune: two runs agree per chat on M1 100%, on M2 70% (30 chats).
