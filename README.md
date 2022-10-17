# AIHub 한국어 음성 데이터 관련 코드

- 데이터셋 이름 : [한국어 음성](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=123)



## Project 디렉토리 구조

```
├─data                # 데이터 폴더
│  ├─KsponSpeech_train
│  │  ├─KsponSpeech_01
│  │  ├─KsponSpeech_02
│  │  ├─KsponSpeech_03
│  │  ├─KsponSpeech_04
│  │  ├─KsponSpeech_05
│  ├─KsponSpeech_scripts
│  │  ├─dev.trn
│  │  ├─eval_clean.trn
│  │  ├─eval_other.trn
│  │  ├─train.trn
│  ├─KsponSpeech_eval
│  │  ├─eval_clean
│  │  ├─eval_other
└─README.md
```

### data

AI 허브에서 다운로드한 데이터를 data 디렉토리 하위 경로로 복사하거나 symbolic link를 설정한다(디렉토리 구조를 참고하여 설정)

#### KsponSpeech_scripts

- dev.trn: 2,545라인
- eval_clean.trn: 3,000라인
- eval_other.trn: 3,000라인
- train.trn: 620,000라인

#### KsponSpeech_eval

- eval_clean: 3,000개
- eval_other: 3,000개