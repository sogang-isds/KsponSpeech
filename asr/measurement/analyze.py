import argparse
import csv
import os
from math import log


def get_annotate_error_candidates(input_file, cer_threshold=0.1, ppl_threshold=0.2, verbose=True):
    cer_candidate_count = 0
    ppl_ref_gt_hyp_count = 0
    ppl_gt_threshold_count = 0
    ppl_ref_lt_hyp_count = 0

    machine_craft_file = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        relevant_count = 0
        total_count = 0

        max_hyp_len = 0
        for i, elem in enumerate(reader):
            total_count += 1
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

            diff_ratio_a = abs(ref_ppl - hyp_ppl) / ref_ppl
            diff_ratio_b = abs(ref_ppl - hyp_ppl) / hyp_ppl

            if diff_ratio_a > ppl_threshold:
                ppl_gt_threshold_count += 1

            if ref_ppl < hyp_ppl:
                ppl_ref_lt_hyp_count += 1

            if ref_ppl > hyp_ppl:
                ppl_ref_gt_hyp_count += 1

            if ref_ppl > hyp_ppl and diff_ratio_a > ppl_threshold and normalized_cer > cer_threshold:
                # if 1 == 1:
                # if normalized_cer > cer_threshold:
                # if diff_ratio_a > ppl_threshold:
                    if verbose:
                        print(f'\nfile: {filename}')
                        print(f'reference: {reference}\tppl: {ref_ppl}')
                        print(f'hypothesis: {hypothesis}\tppl: {hyp_ppl}')
                        print(f'cer: {cer:.4f}, normalized_cer: {normalized_cer:.4f}')
                        print(f'diff_ratio_a: {diff_ratio_a:.4f}, diff_ratio_b: {diff_ratio_b:.4f}')
                        print(f'wil: {wil:.4f}, wip: {wip:.4f}')
                    relevant_count += 1

                    machine_craft_file.append(filename)

    print(f'\n===== Error Candidate Result =====')
    print(f'cer_threshold: {cer_threshold}')
    print(f'ppl_threshold: {ppl_threshold}')
    print(f'detection ratio: {relevant_count/total_count * 100:.2f} ({relevant_count}/{total_count})')
    print(f'(a) |PPL(ref) - PPL(hyp)| > threshold: {ppl_gt_threshold_count}')
    print(f'(b) Normalized CER(hyp) > threshold: {cer_candidate_count}')
    print(f'(c) PPL(ref) > PPL(hyp): {ppl_ref_gt_hyp_count}')
    print(f'(d) PPL(ref) < PPL(hyp): {ppl_ref_lt_hyp_count}')
    print(f'(a)+(b):')


    return machine_craft_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', default='input.csv', type=str)
    args = parser.parse_args()

    machine_craft_file = get_annotate_error_candidates(args.input_file, cer_threshold=0.05, ppl_threshold=0.15, verbose=True)
