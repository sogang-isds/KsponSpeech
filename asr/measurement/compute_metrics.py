import os
import json
import jiwer
import pandas as pd
import argparse
import pprint


def main(args):
    scores = []

    for file in os.listdir(args.result_dir):
        if file.endswith('.csv'):
            data = pd.read_csv(args.result_dir + file)
            data = data.dropna(axis=0)
            result = jiwer.compute_measures(list(data['reference']), list(data['hypothesis']))
            scores.append({file : result})
            scores[-1][file]['cer'] = jiwer.cer(list(data['reference']), list(data['hypothesis']))

    pprint.pprint(scores)

    with open(args.save_path, 'w') as f:
        json.dump(scores, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result_dir', default='../Whisper/result/', type=str)
    parser.add_argument('--save_path', default='../Whisper/result/final_scores.json', type=str)
    args = parser.parse_args()

    main(args)