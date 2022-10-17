import os
import sox
import json
from tqdm import tqdm


def save_to_json(DEST_PATH, data, filename):
    with open(DEST_PATH + filename + '.json', 'w', encoding='utf-8') as f:
        for line in data:
            json.dump(line, f, ensure_ascii=False)
            f.write('\n')


def build_manifest(DATA_PATH, TRN_PATH):
    data = []
    with open(TRN_PATH, 'r') as f:
        print('Processed with', TRN_PATH.split('/')[2].split('.')[0])
        contents = f.read()
        contents = contents.split('\n')

        for content in tqdm(contents):
            if content:
                wav_path = (DATA_PATH + content.split('::')[0][:-1]).replace('.pcm', '.wav')
                text = content.split('::')[1][1:]
                duration = sox.file_info.duration(wav_path)

                manifest = {
                    'audio_filepath': wav_path,
                    'duration': duration,
                    'text': text
                }
                data.append(manifest)

        return data


def build_train_valid_manifest(DATA_PATH):
    train_data = []
    valid_data = []
    for num in tqdm(range(1, 5)):
        speech_dir = DATA_PATH + 'KsponSpeech_0{}/'.format(num)
        print('Processed with', speech_dir)
        for (path, dirs, files) in os.walk(speech_dir):
            for subdirs in dirs:
                if subdirs in ('KsponSpeech_0621', 'KsponSpeech_0622', 'KsponSpeech_0623'):
                    subdir = os.path.join(speech_dir, subdirs)
                    for file in os.listdir(subdir):
                        if file.endswith('.txt'):
                            with open(subdir + '/' + file, 'r') as f:
                                content = f.read()

                            text = content.split('\n')
                            wav_path = subdir + '/' + file.replace('.txt', '.wav')
                            duration = sox.file_info.duration(wav_path)

                            manifest = {
                                'audio_filepath': wav_path,
                                'duration': duration,
                                'text': text
                            }
                            valid_data.append(manifest)

                else:
                    subdir = os.path.join(speech_dir, subdirs)
                    for file in os.listdir(subdir):
                        if file.endswith('.txt'):
                            with open(subdir + '/' + file, 'r') as f:
                                content = f.read()

                            text = content.split('\n')
                            wav_path = subdir + '/' + file.replace('.txt', '.wav')
                            duration = sox.file_info.duration(wav_path)

                            manifest = {
                                'audio_filepath': wav_path,
                                'duration': duration,
                                'text': text
                            }
                            train_data.append(manifest)

    return train_data, valid_data


if __name__ == '__main__':
    DATA_PATH = '../data/'
    TRN_PATH = '../KsponSpeech_scripts/'
    DEST_PATH = '../manifest/'

    if not os.path.isdir(DEST_PATH):
        os.mkdir(DEST_PATH)

    for file in os.listdir(TRN_PATH):
        if file.endswith('.trn'):
            data = build_manifest(DATA_PATH, TRN_PATH + file)
            save_to_json(DEST_PATH, data, file.split('.')[0])

    print('Finished building manifest')