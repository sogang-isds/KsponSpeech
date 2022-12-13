import argparse
import csv
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', default='input.csv', type=str)
    args = parser.parse_args()

    cer_threshold = 0.02
    ppl_threshold = 0.15
    cer_candidate_count = 0
    ppl_candidate_count = 0
    ppl_candidate2_count = 0

    machine_craft_file = []

    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        max_len = 116
        count = 0

        for i, elem in enumerate(reader):

            audio_filepath = elem[0]
            reference = elem[1]
            hypothesis = elem[2]
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

            normalized_cer = cer * hyp_len / max_len

            if normalized_cer > cer_threshold:
                cer_candidate_count += 1

            if ref_ppl > hyp_ppl:
                diff_ratio_a = (ref_ppl - hyp_ppl) / ref_ppl
                diff_ratio_b = (ref_ppl - hyp_ppl) / hyp_ppl

                ppl_candidate_count += 1

                if diff_ratio_a > ppl_threshold:
                    ppl_candidate2_count += 1

                if diff_ratio_a > ppl_threshold and normalized_cer > cer_threshold:
                    print(f'\nfile: {os.path.basename(audio_filepath)}')
                    print(f'reference: {reference}\tppl: {ref_ppl}')
                    print(f'hypothesis: {hypothesis}\tppl: {hyp_ppl}')
                    print(f'cer: {cer:.4f}, normalized_cer: {normalized_cer:.4f}')
                    print(f'diff_ratio_a: {diff_ratio_a:.4f}, diff_ratio_b: {diff_ratio_b:.4f}')
                    print(f'wil: {wil:.4f}, wip: {wip:.4f}')
                    count += 1

    print('===== Result =====')
    print(f'cer_threshold: {cer_threshold}')
    print(f'ppl_threshold: {ppl_threshold}')
    print(f'result count: {count}')
    print(f'cer_candidate_count: {cer_candidate_count}')
    print(f'ppl_candidate_count(ref_ppl > hyp_ppl): {ppl_candidate_count}')
    print(f'ppl_candidate2_count(threshfold): {ppl_candidate2_count}')
