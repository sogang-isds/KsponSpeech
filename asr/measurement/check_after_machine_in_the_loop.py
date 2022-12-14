import os
import json
import pandas as pd
import csv

from asr.measurement.analyze import get_annotate_error_candidates


def check_after_machine_in_the_loop():
    final_reference = []
    human_craft_file = []
    machine_craft_file = []

    with open('../../transcription_corpus_checked.json', 'r') as f:
        data = json.load(f)

    for d in data:
        final_reference.append(d['meta'][0]['text'])

    metric_result_file = '../../eval_clean_add_metrics.csv'
    # metric_result_file = '../../eval_clean_add_metrics_squeezeformer.csv'
    text_clean = pd.read_csv(metric_result_file)

    for file, origin, ref in zip(text_clean['audio_filepath'], text_clean['reference'], final_reference):
        if origin != ref:
            human_craft_file.append(os.path.basename(file))

    machine_craft_file = get_annotate_error_candidates(metric_result_file)

    final_file = []

    for file, origin_ref, change in zip(text_clean['audio_filepath'], text_clean['reference'], final_reference):
        if os.path.basename(file) in machine_craft_file:
            final_file.append(change)
        else:
            final_file.append(origin_ref)

    human_machine_intersection = set(human_craft_file).intersection(set(machine_craft_file))
    print('\n===== Experiment Result =====')
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