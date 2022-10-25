# This is where the an4/ directory will be placed.
# Change this if you don't want the data to be extracted in the current directory.

# NeMo's "core" package
import logging

from nemo.utils.exp_manager import exp_manager
from pytorch_lightning.plugins import DDPPlugin

import nemo
# NeMo's ASR collection - this collections contains complete ASR models and
# building blocks (modules) for ASR
import nemo.collections.asr as nemo_asr

from nemo.core.config import hydra_runner
from omegaconf import OmegaConf, open_dict

@hydra_runner(config_path="./conf/conformer/", config_name="conformer_ctc_bpe")
def main(cfg):
    logging.info(f'Hydra config: {OmegaConf.to_yaml(cfg)}')

    cfg.model.tokenizer.dir = "tmp/tokenizer_spe_bpe_v5000/"  # note this is a directory, not a path to a vocabulary file
    cfg.model.tokenizer.type = "bpe"

    import pytorch_lightning as pl
    # trainer = pl.Trainer(strategy=DDPPlugin(find_unused_parameters=False),
    #                      max_epochs=50,
    #                      log_every_n_steps=100
    #                      )
    trainer = pl.Trainer(**cfg.trainer)
    exp_manager(trainer, cfg.get("exp_manager", None))

    train_manifest = 'manifests/preprocessed/train.json'
    dev_manifest = 'manifests/preprocessed/dev.json'

    # Update paths to dataset
    cfg.model.train_ds.manifest_filepath = train_manifest
    cfg.model.validation_ds.manifest_filepath = dev_manifest

    first_asr_model = nemo_asr.models.EncDecCTCModelBPE(cfg=cfg.model, trainer=trainer)

    from pytorch_lightning.utilities.model_summary import summarize
    summarize(first_asr_model)

    # Start training!!!
    trainer.fit(first_asr_model)

    first_asr_model.save_to("conformer_ctc_bpe_model.nemo")


if __name__ == '__main__':
    main()