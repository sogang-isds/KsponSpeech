import os
import re
import json
from tqdm import tqdm
import argparse

from utils import save_to_json

# reference from https://github.com/sooftware/ksponspeech

PERCENT_FILES = {
    '087797': '퍼센트',
    '215401': '퍼센트',
    '284574': '퍼센트',
    '397184': '퍼센트',
    '501006': '프로',
    '502173': '프로',
    '542363': '프로',
    '581483': '퍼센트'
}


def bracket_filter(sentence, mode='phonetic'):
    new_sentence = str()

    if mode == 'phonetic':
        flag = False

        for ch in sentence:
            if ch == '(' and flag is False:
                flag = True
                continue
            if ch == '(' and flag is True:
                flag = False
                continue
            if ch != ')' and flag is False:
                new_sentence += ch

    elif mode == 'spelling':
        flag = True

        for ch in sentence:
            if ch == '(':
                continue
            if ch == ')':
                if flag is True:
                    flag = False
                    continue
                else:
                    flag = True
                    continue
            if ch != ')' and flag is True:
                new_sentence += ch

    else:
        raise ValueError("Unsupported mode : {0}".format(mode))

    return new_sentence


def special_filter(sentence, mode='phonetic', replace=None):
    SENTENCE_MARK = ['?', '!', '.']
    NOISE = ['o', 'n', 'u', 'b', 'l']
    EXCEPT = ['/', '+', '*', '-', '@', '$', '^', '&', '[', ']', '=', ':', ';', ',', '?', '!', '.']

    new_sentence = str()
    for idx, ch in enumerate(sentence):
        if ch not in SENTENCE_MARK:
            if idx + 1 < len(sentence) and ch in NOISE and sentence[idx + 1] == '/':
                continue

        if ch == '#':
            new_sentence += '샾'

        elif ch == '%':
            if mode == 'phonetic':
                new_sentence += replace
            elif mode == 'spelling':
                new_sentence += '%'

        elif ch not in EXCEPT:
            new_sentence += ch

    pattern = re.compile(r'\s\s+')
    new_sentence = re.sub(pattern, ' ', new_sentence.strip())
    return new_sentence


def sentence_filter(raw_sentence, mode, replace=None):
    return special_filter(bracket_filter(raw_sentence, mode), mode, replace)


def read_preprocess_file(file_path, mode):
    manifest_data = []

    with open(file_path, 'r') as f:
        for line in tqdm(f, desc='Preprocessing manifest'):
            line = line.replace('\n', '')
            text = json.loads(line)['text']
            audio_path = json.loads(line)['audio_filepath']
            duration = json.loads(line)['duration']
            if audio_path[-10:-4] in PERCENT_FILES.keys():
                replace = PERCENT_FILES[audio_path[-10:-4]]
            else:
                replace = None

            new_text = sentence_filter(text, mode=mode, replace=replace)

            manifest = {
                'audio_filepath': audio_path,
                'duration': duration,
                'text': new_text
            }

            manifest_data.append(manifest)

    return manifest_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode',
                        type=str,
                        help='phonetic or spelling',
                        default='phonetic')
    parser.add_argument('--manifest_path',
                        type=str,
                        help='manifest path',
                        default="../asr/nemo/manifests/")
    parser.add_argument('--save_path',
                        type=str,
                        help='save path',
                        default='../asr/nemo/manifests/preprocessed/')
    args = parser.parse_args()

    MANIFEST_PATH = args.manifest_path
    DEST_PATH = args.save_path

    if not os.path.isdir(DEST_PATH):
        os.mkdir(DEST_PATH)

    for file in os.listdir(MANIFEST_PATH):
        if file.endswith('.json') and not 'sample' in file:
            in_file = os.path.join(MANIFEST_PATH, file)
            print(f'Processing: {in_file}')
            data = read_preprocess_file(in_file, mode=args.mode)
            out_file = file.split('.')[0] + '.json'
            save_to_json(DEST_PATH, data, out_file)
            print(f'File saved: {os.path.abspath(os.path.join(DEST_PATH, out_file))}')

    print('Finished preprocessing manifest')
