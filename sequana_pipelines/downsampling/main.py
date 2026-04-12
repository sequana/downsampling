#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import sys

import rich_click as click
from sequana_pipetools import SequanaManager
from sequana_pipetools.options import *

NAME = "downsampling"


help = init_click(
    NAME,
    groups={
        "Pipeline Specific": [
            "--downsampling-input-format",
            "--downsampling-method",
            "--downsampling-percent",
            "--downsampling-max-entries",
            "--downsampling-threads",
        ],
    },
)


@click.command(context_settings=help)
@include_options_from(ClickInputOptions)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickGeneralOptions)
@click.option(
    "--downsampling-input-format",
    "downsampling_input_format",
    default="fastq",
    show_default=True,
    type=click.Choice(["fasta", "fastq", "sam"]),
    help="set input format (only 'fastq', 'fasta', 'sam' supported for now)",
)
@click.option(
    "--downsampling-method",
    "downsampling_method",
    default="random",
    show_default=True,
    type=click.Choice(["random", "random_pct"]),
    help="downsampling method: random (based on read counts) or random_pct (based on a percentage of reads)",
)
@click.option(
    "--downsampling-percent",
    "downsampling_percent",
    default=10.0,
    show_default=True,
    type=float,
    help="percentage of reads to select. Use with method 'random_pct' only",
)
@click.option(
    "--downsampling-max-entries",
    "downsampling_max_entries",
    default=1000,
    show_default=True,
    type=int,
    help="max entries (reads, alignments) to select. Use with method 'random' only",
)
@click.option(
    "--downsampling-threads",
    "downsampling_threads",
    default=4,
    show_default=True,
    type=int,
    help="max threads to use with pigz",
)
def main(**options):

    if options["from_project"]:
        click.echo("--from-project Not yet implemented")
        sys.exit(1)

    # the real stuff is here
    manager = SequanaManager(options, NAME)
    manager.setup()

    options = manager.options
    cfg = manager.config.config

    from sequana_pipetools import logger

    logger.setLevel(options.level)
    logger.name = "sequana_downsampling"

    manager.fill_data_options()

    # --------------------------------------------------- downsampling
    cfg.downsampling.input_format = options.downsampling_input_format
    cfg.downsampling.method = options.downsampling_method
    cfg.downsampling.percent = options.downsampling_percent
    cfg.downsampling.max_entries = options.downsampling_max_entries
    cfg.downsampling.threads = options.downsampling_threads

    # If input format is fasta, adjust input pattern default
    if options.downsampling_input_format == "fasta" and options.input_pattern == "*fastq.gz":
        cfg.input_pattern = "*fasta.gz"

    logger.info(f"Input data should be {cfg.downsampling.input_format}")
    if cfg.downsampling.method == "random":
        logger.info(f"Your data will be downsampled randomly keeping {cfg.downsampling.max_entries} reads")
    elif cfg.downsampling.method == "random_pct":
        logger.info(f"Your data will be downsampled randomly keeping {cfg.downsampling.percent}% of the reads")

    manager.teardown()


if __name__ == "__main__":
    main()
