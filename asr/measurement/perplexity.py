import argparse
import csv

import torch
from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

device = "cuda"
model_id = "skt/kogpt2-base-v2"
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)


def predict_perplexity(text):
    input_ids = tokenizer.encode(text, return_tensors='pt')

    max_length = model.config.n_positions
    stride = 512
    seq_len = input_ids.size(1)

    nlls = []
    prev_end_loc = 0
    for begin_loc in tqdm(range(0, seq_len, stride)):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc  # may be different from stride on last loop
        input_ids = input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)

            # loss is calculated using CrossEntropyLoss which averages over input tokens.
            # Multiply it with trg_len to get the summation instead of average.
            # We will take average over all the tokens to get the true average
            # in the last step of this example.
            neg_log_likelihood = outputs.loss * trg_len

        nlls.append(neg_log_likelihood)

        prev_end_loc = end_loc
        if end_loc == seq_len:
            break

    if len(nlls) > 0:
        ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
        return ppl.cpu().numpy()
    else:
        return 'nan'


def write_line(f, line):
    print(line)
    f.write(line + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', default='input.csv', type=str)
    parser.add_argument('--output_file', default='output.csv', type=str)
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f, \
            open(args.output_file, 'w', encoding='utf-8') as fw:

        reader = csv.reader(f)
        header = next(reader)

        writer = csv.writer(fw)

        output_header = header.copy()
        output_header.extend(['ref_ppl', 'hyp_ppl'])
        writer.writerow(output_header)

        for i, elem in enumerate(reader):
            audio_filepath = elem[0]
            reference = elem[1]
            hypothesis = elem[2]

            ref_ppl = predict_perplexity(reference)
            hyp_ppl = predict_perplexity(hypothesis)

            elem.append(ref_ppl)
            elem.append(hyp_ppl)

            writer.writerow(elem)
