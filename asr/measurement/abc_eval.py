from jiwer import wer, wil, wip, cer
import re
from tqdm import tqdm

def transform_alpha(sent):
    transform_dict = {
        "a": "에이",
        "b": "비",
        "c": "씨",
        "d": "디",
        "e": "이",
        "f": "에프",
        "g": "지",
        "h": "에이치",
        "i": "아이",
        "j": "제이",
        "k": "케이",
        "l": "엘",
        "m": "엠",
        "n": "엔",
        "o": "오",
        "p": "피",
        "q": "큐",
        "r": "알",
        "s": "에스",
        "t": "티",
        "u": "유",
        "v": "브이",
        "w": "더블유",
        "x": "엑스",
        "y": "와이",
        "z": "제트",
    }
    new_sent = list(sent)
    for i, ch in enumerate(sent):
        if 'a' <= ch <= 'z':
            new_sent[i] = transform_dict[ch]

    return "".join(new_sent)

data = [{'audio_filepath':x.split(",")[0],
         'reference':x.split(",")[1],
         'hypothesis':x.split(",")[2].replace("\n","")} for x in open("train_result.csv").readlines()[1:]]
# audio_filepath, reference, hypothesis

alpha_data = []
pattern = re.compile(r'[a-zA-Z]')
for i, x in tqdm(enumerate(data)):
    ref = x['reference']
    hypo = x['hypothesis']



    if pattern.match(ref):
        x['wer'] = str(wer(ref,hypo))
        x['wil'] = str(wil(ref,hypo))
        x['wip'] = str(wip(ref,hypo))
        x['cer'] = str(cer(ref,hypo))
        alpha_data.append(x)

fp = open("only_alphabet_scores.csv",'w')
fp.write(",".join(['audio_filepath', 'reference', 'hypothesis', 'wer', 'wil', 'wip', 'cer'])+'\n')
fp.writelines([",".join(x.values())+'\n' for x in alpha_data])



alpha_data = []
pattern = re.compile(r'[a-zA-Z]')
for i, x in tqdm(enumerate(data)):
    ref = x['reference']
    hypo = x['hypothesis']

    if pattern.match(ref):
        ref = transform_alpha(x['reference'])
        hypo = transform_alpha(x['hypothesis'])
        x['transformed_reference'] = ref
        x['transformed_hypothesis'] = hypo
        x['wer'] = str(wer(ref,hypo))
        x['wil'] = str(wil(ref,hypo))
        x['wip'] = str(wip(ref,hypo))
        x['cer'] = str(cer(ref,hypo))
        alpha_data.append(x)

fp = open("transformed_alphabet_scores.csv",'w')
fp.write(",".join(['audio_filepath', 'reference', 'hypothesis', 'transformed_reference', 'transformed_hypothesis', 'wer', 'wil', 'wip', 'cer'])+'\n')
fp.writelines([",".join(x.values())+'\n' for x in alpha_data])