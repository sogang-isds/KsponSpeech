# Whisper ASR

Whisper 모델로 결과를 확인하고 싶은 데이터셋을 argument로 넣어주면, inference 수행

```bash
python test_whisper.py --train --dev --eval_other --eval_clean
```

jiwer package로 WER, CER 등 metric 계산

```bash
python compute_measure.py --result_dir result/ --save_path result/final_scores.json
```