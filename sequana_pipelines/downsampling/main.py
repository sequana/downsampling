import sys
import os
import argparse

from sequana.pipelines_common import *
from sequana.snaketools import Module
from sequana import logger
logger.level = "INFO"

col = Colors()

NAME = "downsampling"
m = Module(NAME)
m.is_executable()


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME):
        usage = col.purple(
            """This script prepares the sequana pipeline downsampling layout to
            include the Snakemake pipeline and its configuration file ready to
            use.

            In practice, it copies the config file and the pipeline into a
            directory (downsampling) together with an executable script

            For a local run, use :

                sequana_pipelines_downsampling --input-directory PATH_TO_DATA 

            For a run on a SLURM cluster:

                sequana_pipelines_downsampling --input-directory PATH_TO_DATA 

        """
        )
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)
        so = InputOptions(add_input_readtag=False, add_is_paired=False)
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline")

        pipeline_group.add_argument("--downsampling-input-format", 
            default="fastq", type=str, 
            help="set input format (only 'fastq' supported for now)")


def main(args=None):

    if args is None:
        args = sys.argv

    options = Options(NAME).parse_args(args[1:])

    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    cfg = manager.config.config
    # EXAMPLE TOREPLACE WITH YOUR NEEDS
    cfg.input_directory = os.path.abspath(options.input_directory)
    manager.exists(cfg.input_directory)
    cfg.input_pattern = options.input_pattern
    cfg.input_readtag = None
    #cfg.paired_data = False

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
