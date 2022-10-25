# NeMo ASR

## Tokenizer 학습

```bash
python process_asr_text_tokenizer.py --manifest manifests/preprocessed/train.json,manifests/preprocessed/dev/json --data_root tmp --tokenizer spe --vocab_size 5000
```



## ASR 학습

### Conformer-CTC

```bash
python asr_ctc_model_bpe_train_hydra.py --config-path=./conf/conformer/ --config-name=conformer_ctc_bpe model.optim.lr=0.01
```

### Squeezeformer-CTC

```bash
python asr_ctc_model_bpe_train_hydra.py --config-path=./conf/squeezeformer/ --config-name=squeezeformer_ctc_bpe
```

학습 시 distributed_backend=nccl 이후에 안넘어 가는 경우 아래와 같이 변경 후 다시 실행

```bash
export PL_TORCH_DISTRIBUTED_BACKEND=gloo
```

