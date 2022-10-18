# NeMo ASR

## Tokenizer 학습

```bash
python process_asr_text_tokenizer.py --manifest manifests/train.json,manifests/dev.json --data_root tmp --tokenizer spe --vocab_size 5000
```


## ASR 학습

### Conformer-CTC

```bash
python asr_conformer_ctc_train_hydra.py --config-name=conformer_ctc_bpe model.optim.lr=0.01
```

