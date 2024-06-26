import os
import sox
from tqdm import tqdm

from utils import save_to_json


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default=False, action='store_true')
    parser.add_argument('--dev', default=False, action='store_true')
    parser.add_argument('--test', default=False, action='store_true')
    args = parser.parse_args()

    return args


def build_manifest(DATA_PATH, TRN_PATH):
    data = []
    with open(TRN_PATH, 'r') as f:
        print('Processed with', TRN_PATH.split('/')[-1].split('.')[0], 'data')
        contents = f.read()
        contents = contents.split('\n')

        for content in tqdm(contents):
            if content:
                wav_path = (DATA_PATH + content.split('::')[0][:-1]).replace('.pcm', '.wav')
                text = content.split('::')[1][1:]
                duration = sox.file_info.duration(wav_path)

                manifest = {
                    'audio_filepath': '../' + wav_path,
                    'duration': duration,
                    'text': text
                }
                data.append(manifest)

        return data


def main():
    args = parse_args()

    if not (args.train or args.dev or args.test):
        print('Please select the data you want to build manifest')

    else:
        if args.train:
            DATA_PATH = '../data/KsponSpeech_train/'
            TRN_PATH = '../data/KsponSpeech_scripts/train.trn'
            DEST_PATH = '../asr/nemo/manifests/'

            if not os.path.isdir(DEST_PATH):
                os.mkdir(DEST_PATH)

            data = build_manifest(DATA_PATH, TRN_PATH)
            out_file = TRN_PATH.split('/')[-1].split('.')[0] + '.json'
            save_to_json(DEST_PATH, data, out_file)
            print(f'File saved: {os.path.abspath(os.path.join(DEST_PATH, out_file))}')

        if args.dev:
            DATA_PATH = '../data/KsponSpeech_train/'
            TRN_PATH = '../data/KsponSpeech_scripts/dev.trn'
            DEST_PATH = '../asr/nemo/manifests/'

            if not os.path.isdir(DEST_PATH):
                os.mkdir(DEST_PATH)

            data = build_manifest(DATA_PATH, TRN_PATH)
            out_file = TRN_PATH.split('/')[-1].split('.')[0] + '.json'
            save_to_json(DEST_PATH, data, out_file)
            print(f'File saved: {os.path.abspath(os.path.join(DEST_PATH, out_file))}')

        if args.test:
            DATA_PATH = '../data/'
            TRN_PATH = '../data/KsponSpeech_scripts/'
            DEST_PATH = '../asr/nemo/manifests/'

            if not os.path.isdir(DEST_PATH):
                os.mkdir(DEST_PATH)

            for file in os.listdir(TRN_PATH):
                if file.endswith('.trn') and file.startswith('eval'):
                    data = build_manifest(DATA_PATH, TRN_PATH + file)
                    out_file = file.split('.')[0] + '.json'
                    save_to_json(DEST_PATH, data, out_file)
                    print(f'File saved: {os.path.abspath(os.path.join(DEST_PATH, out_file))}')

        print('Finished building manifest')


if __name__ == '__main__':
    main()
