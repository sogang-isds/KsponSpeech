import os
import json
import jiwer
import pandas as pd
import argparse
import pprint


def main(result_dir, save_path):
    scores = []

    for file in os.listdir(result_dir):
        if file.endswith('.csv'):
            data = pd.read_csv(result_dir + file)
            result = jiwer.compute_measures(list(data['reference']), list(data['hypothesis']))
            scores.append({file : result})
            scores[-1][file]['cer'] = jiwer.cer(list(data['reference']), list(data['hypothesis']))

    pprint.pprint(scores)

    with open(save_path, 'w') as f:
        json.dump(scores, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result_dir', default='result/', type=str)
    parser.add_argument('--save_path', default='result/final_scores.json', type=str)
    args = parser.parse_args()

    main(args.result_dir, args.save_path)