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
import argparse
import os
import shutil
import subprocess
import sys

import click_completion
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
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions, input_pattern="*.fasta", add_input_readtag=False)
@include_options_from(ClickGeneralOptions)
@click.option(
    "--downsampling-input-format",
    default="fastq",
    type=click.Choice(["fasta", "fastq"]),
    help="set input format (only 'fastq', 'fasta', supported for now)",
)
@click.option(
    "--downsampling-method",
    default="random",
    type=click.Choice(["random", "random_pct"]),
    help="""set the downsampling method to be random based on read
                counts (random) on read percentage (random_pct))""",
)
@click.option(
    "--downsampling-percent",
    default=10,
    type=click.FLOAT,
    help="""Percentage of reads to select. Use with method *random_pct* only""",
)
@click.option(
    "--downsampling-max-entries",
    default=1000,
    type=click.INT,
    help="""max entries (reads, alignement) to select. Use with method *random* only""",
)
@click.option("--downsampling-threads", default=4, type=click.INT, help="""max threads to use with pigz""")
def main(**options):
    if options["from_project"]:
        click.echo("--from-project Not yet implemented")
        sys.exit(1)

    # the real stuff is here
    manager = SequanaManager(options, NAME)
    manager.setup()

    options = manager.options
    cfg = manager.config.config

    # manager.fill_data_options()

    cfg.input_directory = os.path.abspath(options.input_directory)
    cfg.input_pattern = options.input_pattern
    # cfg.input_readtag = options.input_readtag

    # --------------------------------------------------- downsampling
    cfg.downsampling.input_format = options.downsampling_input_format
    cfg.downsampling.method = options.downsampling_method
    cfg.downsampling.percent = options.downsampling_percent
    cfg.downsampling.max_entries = options.downsampling_max_entries
    cfg.downsampling.threads = options.downsampling_threads

    # by default,
    if options.downsampling_input_format == "fasta" and options.input_pattern == "*fastq.gz":
        cfg.input_pattern = "*fasta.gz"

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.

    from sequana_pipetools import logger

    logger.info("Input data should be {}".format(cfg.downsampling.input_format))
    if cfg.downsampling.method == "random":
        logger.info("Your data will be downsampled randomly keeping {} reads".format(cfg.downsampling.max_entries))
    elif cfg.downsampling.method == "random_pct":
        logger.info("Your data will be downsampled randomly keeping {}% of the reads".format(cfg.downsampling.percent))

    manager.teardown()


if __name__ == "__main__":
    main()
