import argparse
import csv
import os
from math import log


def get_annotate_error_candidates(input_file):
    cer_threshold = 0.0944
    # cer_threshold = 0.25
    ppl_threshold = 0.15
    cer_candidate_count = 0
    ppl_candidate_count = 0
    ppl_candidate2_count = 0

    machine_craft_file = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        count = 0

        max_hyp_len = 0
        for i, elem in enumerate(reader):
            reference = elem[1]
            hypothesis = elem[2]

            ref_len = len(reference)
            hyp_len = len(hypothesis)

            if hyp_len > max_hyp_len:
                max_hyp_len = hyp_len

        print(f'max_hyp_len: {max_hyp_len}')
        f.seek(0)

        for i, elem in enumerate(reader):

            audio_filepath = elem[0]
            reference = elem[1]
            hypothesis = elem[2]

            filename = os.path.basename(audio_filepath)

            try:
                ref_ppl = float(elem[3])
                hyp_ppl = float(elem[4])
            except ValueError:
                continue

            cer = float(elem[5])
            wer = float(elem[6])
            wil = float(elem[11])
            wip = float(elem[12])

            ref_len = len(reference)
            hyp_len = len(hypothesis)

            normalized_cer = cer * log(hyp_len) / log(max_hyp_len)
            # normalized_cer = wer * log(hyp_len) / log(max_hyp_len)
            # normalized_cer = cer

            if normalized_cer > cer_threshold:
                cer_candidate_count += 1

            if ref_ppl > hyp_ppl:
                # if ref_ppl < hyp_ppl:
                diff_ratio_a = abs(ref_ppl - hyp_ppl) / ref_ppl
                diff_ratio_b = abs(ref_ppl - hyp_ppl) / hyp_ppl

                ppl_candidate_count += 1

                if diff_ratio_a > ppl_threshold:
                    ppl_candidate2_count += 1

                if diff_ratio_a > ppl_threshold and normalized_cer > cer_threshold:
                    # if normalized_cer2 > cer_threshold:
                    # if diff_ratio_a > ppl_threshold:
                    print(f'\nfile: {filename}')
                    print(f'reference: {reference}\tppl: {ref_ppl}')
                    print(f'hypothesis: {hypothesis}\tppl: {hyp_ppl}')
                    print(f'cer: {cer:.4f}, normalized_cer: {normalized_cer:.4f}')
                    print(f'diff_ratio_a: {diff_ratio_a:.4f}, diff_ratio_b: {diff_ratio_b:.4f}')
                    print(f'wil: {wil:.4f}, wip: {wip:.4f}')
                    count += 1

                    machine_craft_file.append(filename)

    print(f'\n===== Error Candidate Result =====')
    print(f'cer_threshold: {cer_threshold}')
    print(f'ppl_threshold: {ppl_threshold}')
    print(f'result count: {count}')
    print(f'cer_candidate_count: {cer_candidate_count}')
    print(f'ppl_candidate_count(ref_ppl > hyp_ppl): {ppl_candidate_count}')
    print(f'ppl_candidate2_count(threshfold): {ppl_candidate2_count}')

    return machine_craft_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', default='input.csv', type=str)
    args = parser.parse_args()

    machine_craft_file = get_annotate_error_candidates(args.input_file)
