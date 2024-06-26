import whisper
import torch
import os
import json
from tqdm import tqdm
import numpy as np
import pandas as pd
import jiwer
from whisper.normalizers import BasicTextNormalizer

from scipy.io import wavfile


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train',  default=False, action='store_true')
    parser.add_argument('--dev',  default=False,  action='store_true')
    parser.add_argument('--eval_clean',  default=False, action='store_true')
    parser.add_argument('--eval_other', default=False, action='store_true')
    parser.add_argument('--cuda', default='cuda:1', type=str)
    args = parser.parse_args()

    return args


def read_manifest(path):
    manifest = []
    with open(path, 'r') as f:
        for line in tqdm(f, desc='Reading manifest'):
            line = line.replace('\n', '')
            manifest.append(json.loads(line))

    return manifest


def inference(manifest_path, model, transcribe_options):
    manifest_data = read_manifest(manifest_path)
    file_name = manifest_path.split('/')[-1].split('.')[0]

    audio_filepaths = []
    references = []
    transcriptions = []

    for i in tqdm(manifest_data, desc='Inference'):
        audio_filepath = i['audio_filepath']
        # audio = torch.from_numpy(wavfile.read(audio_filepath)[1].copy())
        text = i['text']

        audio = whisper.load_audio(audio_filepath)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        hypothesis = model.decode(mel, transcribe_options)

        audio_filepaths.append(audio_filepath)
        transcriptions.append(hypothesis.text)
        references.append(text)

    data = pd.DataFrame(dict(audio_filepath=audio_filepaths, reference=references, hypothesis=transcriptions))
    data.to_csv(f'result/{file_name}_result.csv', index=False, encoding="utf-8-sig")

    normalizer = BasicTextNormalizer()
    data["hypothesis_clean"] = [normalizer(text) for text in data["hypothesis"]]
    data["reference_clean"] = [normalizer(text) for text in data["reference"]]
    data.to_csv(f'result/{file_name}_result.csv', index=False, encoding="utf-8-sig")

    # wer = jiwer.wer(list(data["reference_clean"]), list(data["hypothesis_clean"]))
    # print(f"WER: {wer * 100:.2f} %")


def main():
    args = parse_args()

    if not (args.train or args.dev or args.eval_clean or args.eval_other):
        print('Please select the data you want to inference')

    else:
        print("Loading model...")
        model = whisper.load_model("base", device=args.cuda)
        print(
            f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
            f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
        )

        options = dict(language="Korean", beam_size=5)
        transcribe_options = whisper.DecodingOptions(fp16=False, task='transcribe', without_timestamps=True, **options)

        if not os.path.isdir('result'):
            os.mkdir('result')

        if args.train:
            manifest_path = '../nemo/manifests/preprocessed/train.json'
            inference(manifest_path, model, transcribe_options)

        elif args.dev:
            manifest_path = '../nemo/manifests/preprocessed/dev.json'
            inference(manifest_path, model, transcribe_options)

        elif args.eval_clean:
            manifest_path = '../nemo/manifests/preprocessed/eval_clean.json'
            inference(manifest_path, model, transcribe_options)

        else:
            manifest_path = '../nemo/manifests/preprocessed/eval_other.json'
            inference(manifest_path, model, transcribe_options)


if __name__ == '__main__':
    main()