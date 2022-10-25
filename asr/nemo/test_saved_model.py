import os
import logging
import pandas as pd
from argparse import ArgumentParser

import torch

# NeMo's ASR collection - this collections contains complete ASR models and
# building blocks (modules) for ASR
import nemo.collections.asr as nemo_asr
from nemo.collections.asr.metrics.wer import word_error_rate
from nemo.utils import logging

try:
    from torch.cuda.amp import autocast
except ImportError:
    from contextlib import contextmanager

    @contextmanager
    def autocast(enabled=None):
        yield


def main():
    parser = ArgumentParser()
    parser.add_argument("--asr_model_path", type=str, default="conformer_ctc_bpe_model.nemo", help="Path to ASR model to use for inference")
    parser.add_argument("--test_path", type=str, default="manifests/preprocessed/eval_clean.json", help="path to test manifest json file")
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--dont_normalize_text", default=False, action='store_true',help="Turn off trasnscript normalization. Recommended for non-English.")
    parser.add_argument("--use_cer", default=True, action='store_true', help="Use Character Error Rate as the evaluation metric")
    parser.add_argument("--use_wer", default=True, action='store_true', help="Use Word Error Rate as the evaluation metric")
    args = parser.parse_args()
    torch.set_grad_enabled(False)

    asr_model = nemo_asr.models.EncDecCTCModelBPE.restore_from(restore_path='conformer_ctc_bpe_model.nemo')
    asr_model.setup_test_data(
        test_data_config={
            'sample_rate': 16000,
            'manifest_filepath': args.test_path,
            'labels': asr_model.decoder.vocabulary,
            'batch_size': args.batch_size,
            'normalize_transcripts': not args.dont_normalize_text,
        }
    )

    can_gpu = torch.cuda.is_available()
    if can_gpu:
        asr_model = asr_model.cuda()

    asr_model.eval()
    labels_map = dict([(i, asr_model.decoder.vocabulary[i]) for i in range(len(asr_model.decoder.vocabulary))])

    hypotheses = []
    references = []
    for test_batch in asr_model.test_dataloader():
        if can_gpu:
            test_batch = [x.cuda() for x in test_batch]
        with autocast():
            log_probs, encoded_len, greedy_predictions = asr_model(
                input_signal=test_batch[0], input_signal_length=test_batch[1]
            )
            for prediction in asr_model._wer.decoding.ctc_decoder_predictions_tensor(greedy_predictions)[0]:
                hypotheses.append(prediction)

        for batch_ind in range(greedy_predictions.shape[0]):
            seq_len = test_batch[3][batch_ind].cpu().detach().numpy()
            seq_ids = test_batch[2][batch_ind].cpu().detach().numpy()
            reference = asr_model._wer.decoding.decode_tokens_to_str(seq_ids[0:seq_len])
            references.append(reference)
        del test_batch

    if args.use_wer:
        wer_value = word_error_rate(hypotheses=hypotheses, references=references, use_cer=False)
        logging.info(f'Got WER of {wer_value}.')
    if args.use_cer:
        cer_value = word_error_rate(hypotheses=hypotheses, references=references, use_cer=True)
        logging.info(f'Got CER of {cer_value}.')

    data = pd.DataFrame(dict(reference=references, hypothesis=hypotheses))
    file_name = args.test_path.split('/')[-1].split('.')[0]

    if not os.path.isdir('result'):
        os.mkdir('result')
    data.to_csv(f'result/{file_name}_result.csv', index=False, encoding="utf-8-sig")
    logging.info(f'Prediction Result saved: result/{file_name}_result.csv')


if __name__ == '__main__':
    main()