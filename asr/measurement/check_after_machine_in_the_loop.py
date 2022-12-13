import os
import json
import pandas as pd
import csv


def check_after_machine_in_the_loop():
    final_reference = []
    human_craft_file = []
    machine_craft_file = []

    with open('../../transcription_corpus_checked.json', 'r') as f:
        data = json.load(f)

    for d in data:
        final_reference.append(d['meta'][0]['text'])

    text_clean = pd.read_csv('../../eval_clean_add_metrics.csv')

    for file, origin, ref in zip(text_clean['audio_filepath'], text_clean['reference'], final_reference):
        if origin != ref:
            human_craft_file.append(os.path.basename(file))

    with open('../../eval_clean_add_metrics.csv', 'r', encoding='utf-8') as f:
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
            hyp_len = len(hypothesis)

            normalized_cer = cer * hyp_len / max_len

            if ref_ppl > hyp_ppl:
                diff_ratio_a = (ref_ppl - hyp_ppl) / ref_ppl

                if diff_ratio_a > 0.15 and normalized_cer > 0.02:
                    machine_craft_file.append(os.path.basename(audio_filepath))
                    count += 1

    final_file = []

    for file, origin_ref, change in zip(text_clean['audio_filepath'], text_clean['reference'], final_reference):
        if os.path.basename(file) in machine_craft_file:
            final_file.append(change)
        else:
            final_file.append(origin_ref)

    human_machine_intersection = set(human_craft_file).intersection(set(machine_craft_file))
    print('Human_machine_intersection: ', len(human_machine_intersection))
    print('Human in the loop: ', len(human_craft_file))
    print('Machine in the loop: ', len(machine_craft_file))
    print("Human & Machine intersection / Machine in the loop", len(human_machine_intersection) / len(machine_craft_file))

    from evaluate import load
    cer = load("cer")

    print("\n원래 CER: ", cer.compute(predictions=list(text_clean['hypothesis']), references=list(text_clean['reference'])))
    print("machine-in-the-loop으로 바꿨다 가정했을 때: ", cer.compute(predictions=list(text_clean['hypothesis']), references=final_file))
    print("only human으로만 바꿨을 때", cer.compute(predictions=list(text_clean['hypothesis']), references=final_reference))


if __name__ == '__main__':
    check_after_machine_in_the_loop()