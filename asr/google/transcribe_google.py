import argparse
import speech_recognition as sr
from pprint import pprint


def recognize_google(file):
    r = sr.Recognizer()
    test_speech = sr.AudioFile(file)
    with test_speech as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    result = r.recognize_google(audio, language='ko-KR', show_all=True)

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, type=str)
    args = parser.parse_args()

    results = recognize_google(args.file)
    pprint(results)