import os
import jiwer
import pandas as pd
import argparse


def main(args):
    for file in os.listdir(args.result_dir):
        wers = []
        cers = []
        if file.endswith('.csv'):
            data = pd.read_csv(args.result_dir + file)
            for reference, hypothesis in zip (data['reference'], data['hypothesis']):
                try:
                    wer = jiwer.wer(reference, hypothesis)
                    cer = jiwer.cer(reference, hypothesis)
                except ValueError:
                    wer = ''
                    cer = ''

                wers.append(wer)
                cers.append(cer)

            data['wer'] = wers
            data['cer'] = cers

            file_name = file.split('.')[0]
            if not os.path.isdir(args.save_dir):
                os.mkdir(args.save_dir)
            data.to_csv(f'{args.save_dir}/{file_name}_wer_cer.csv', index=False, encoding="utf-8-sig")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result_dir', default='../Whisper/result/', type=str)
    parser.add_argument('--save_dir', default='../Whisper/result/score_per_sentence/', type=str)
    args = parser.parse_args()

    main(args)