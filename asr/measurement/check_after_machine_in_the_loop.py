import os
import json
import pandas as pd

from asr.measurement.analyze import get_annotate_error_candidates


def check_after_machine_in_the_loop():
    modified_text_list = []
    human_craft_file = []
    machine_craft_file = []

    with open('../../transcription_corpus_checked.json', 'r') as f:
        data = json.load(f)

    for d in data:
        modified_text_list.append(d['meta'][0]['text'])

    metric_result_file = '../../eval_clean_add_metrics.csv'
    # metric_result_file = '../../eval_clean_add_metrics_squeezeformer.csv'
    text_clean = pd.read_csv(metric_result_file)

    pred_list = list(text_clean['hypothesis'])
    truth_list = list(text_clean['reference'])
    filepath_list = list(text_clean['audio_filepath'])

    for file, origin, ref in zip(filepath_list, truth_list, modified_text_list):
        if origin != ref:
            human_craft_file.append(os.path.basename(file))

    cer_thresholds = [0.05]
    ppl_thresholds = [0.15]
    for cer_threshold in cer_thresholds:
        for ppl_threshold in ppl_thresholds:
            machine_craft_file = get_annotate_error_candidates(metric_result_file,
                                                               cer_threshold=cer_threshold,
                                                               ppl_threshold=ppl_threshold,
                                                               verbose=False)

            mixed_list = []

            for file, origin_text, modified_text in zip(filepath_list, truth_list, modified_text_list):
                if os.path.basename(file) in machine_craft_file:
                    mixed_list.append(modified_text)
                else:
                    mixed_list.append(origin_text)

            human_machine_intersection = set(human_craft_file).intersection(set(machine_craft_file))
            precision = len(human_machine_intersection) / len(machine_craft_file)
            recall = len(human_machine_intersection) / len(human_craft_file)
            f1_score = 2 * (precision * recall) / (precision + recall)

            print('\n===== Experiment Result =====')
            print('Human_machine_intersection: ', len(human_machine_intersection))
            print('Human in the loop: ', len(human_craft_file))
            print('Machine in the loop: ', len(machine_craft_file))
            print(f"Machine precision: {precision:.4f}")
            print(f"Machine recall: {recall:.4f}")
            print(f"Machine F1-score: {f1_score:.4f}")
            print(f'{precision:.2f}\t{recall:.2f}\t{f1_score:.2f}')

            from evaluate import load
            cer = load("cer")

            print(f"\n원래 CER: {cer.compute(predictions=pred_list, references=truth_list):.4f}")
            print(f"machine-in-the-loop으로 바꿨다 가정했을 때: {cer.compute(predictions=pred_list, references=mixed_list):.4f}")
            print(f"only human으로만 바꿨을 때: {cer.compute(predictions=pred_list, references=modified_text_list):.4f}")


if __name__ == '__main__':
    check_after_machine_in_the_loop()
