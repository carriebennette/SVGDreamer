# -*- coding: utf-8 -*-
# Author: ximing xing
# Description: the main func of this project.
# Copyright (c) 2023, XiMing Xing.

import os
import sys
from functools import partial

from accelerate.utils import set_seed
import omegaconf

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from svgdreamer.utils import render_batch_wrap, get_seed_range
from svgdreamer.pipelines.SVGDreamer_pipeline import SVGDreamerPipeline


def main():
    # Load YAML configuration manually
    with open("conf/config.yaml", "r") as file:
        cfg = yaml.safe_load(file)

    # Simulate the DictConfig structure from Hydra
    class ConfigNamespace:
        def __init__(self, dictionary):
            for key, value in dictionary.items():
                setattr(self, key, value)

    cfg = ConfigNamespace(cfg)

    # Set seed
    set_seed(cfg.seed)
    seed_range = get_seed_range(cfg.srange) if cfg.multirun else None

    # Render function
    render_batch_fn = partial(render_batch_wrap, cfg=cfg, seed_range=seed_range)

    if not cfg.multirun:
        pipe = SVGDreamerPipeline(cfg)
        pipe.painterly_rendering(cfg.prompt)
    else:
        render_batch_fn(pipeline=SVGDreamerPipeline, text_prompt=cfg.prompt, target_file=None)


if __name__ == '__main__':
    main()
