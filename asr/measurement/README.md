## 예측 데이터셋을 가지고 성능 측정  

jiwer package로 train을 제외한 저장된 나머지 데이터셋 (dev, eval_clean, eval_other)에 대해, 저장된 모델의 WER, CER 등 metrics를 계산한다.

```bash
python compute_metrics.py --result_dir ../Whisper/result/ --save_path ../Whisper/result/final_scores.json
```

예측 결과가 저장된 csv 파일을 가지고, 문장 별로 WER, CER을 계산한다.

```bash
python cer_per_sentence.py --result_dir ../Whisper/result/ --save_path ../Whisper/result/final_scores.json
```