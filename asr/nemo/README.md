# NeMo ASR

## Tokenizer 학습

```bash
python process_asr_tokenizer.py --manifest test_manifest.json --data_root tmp --tokenizer spe --vocab_size 5000
```



## ASR 학습

### Conformer-CTC

```bash
python asr_conformer_ctc_train_hydra.py --config-name=conformer_ctc_bpe model.optim.lr=0.01
```

학습 시 distributed_backend=nccl 이후에 안넘어 가는 경우 아래와 같이 변경 후 다시 실행

```bash
export PL_TORCH_DISTRIBUTED_BACKEND=gloo
```

