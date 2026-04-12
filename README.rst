
.. image:: https://badge.fury.io/py/sequana-downsampling.svg
     :target: https://pypi.python.org/pypi/sequana-downsampling

.. image:: https://github.com/sequana/downsampling/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/downsampling/actions/workflows

.. image:: https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg
    :target: https://pypi.python.org/pypi/sequana-downsampling
    :alt: Python 3.10 | 3.11 | 3.12

.. image:: https://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: https://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI


This is the **downsampling** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project.

:Overview: Downsample NGS data sets (FastQ or FastA).
:Input: A set of FastQ or FastA files (single or paired-end).
:Output: Downsampled FastQ or FastA files.
:Status: Production
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi.org/10.21105/joss.00352


Installation
~~~~~~~~~~~~

::

    pip install sequana_downsampling --upgrade

You will also need ``pigz`` available on your PATH.


Quick Start
~~~~~~~~~~~

**1. Set up the pipeline**::

    sequana_downsampling --input-directory DATAPATH

**2. Run the pipeline**::

    cd downsampling
    bash downsampling.sh


Usage
~~~~~

::

    sequana_downsampling --help

Key pipeline-specific options:

``--downsampling-input-format``
    Input format: ``fastq`` (default), ``fasta``, or ``sam``.

``--downsampling-method``
    ``random`` (default, keeps a fixed number of reads) or ``random_pct``
    (keeps a percentage of reads).

``--downsampling-max-entries``
    Number of reads to keep when using ``random`` (default: 1000).

``--downsampling-percent``
    Percentage of reads to keep when using ``random_pct`` (default: 10).

``--downsampling-threads``
    Number of threads used by ``pigz`` to compress output (default: 4).

Examples::

    sequana_downsampling --input-directory DATAPATH \
        --downsampling-method random --downsampling-max-entries 100

    sequana_downsampling --input-directory DATAPATH \
        --downsampling-method random_pct --downsampling-percent 10 \
        --downsampling-input-format fasta --input-pattern "*.fasta"

Run on a SLURM cluster::

    cd downsampling
    sbatch downsampling.sh

Or drive Snakemake directly::

    snakemake -s downsampling.rules --cores 4 --stats stats.txt


Requirements
~~~~~~~~~~~~

The following tools must be available (install via conda/bioconda)::

    mamba env create -f environment.yml

- **sequana** — FastQ/FastA selection (Python API)
- **pigz** — parallel gzip compression of outputs


Pipeline overview
~~~~~~~~~~~~~~~~~

The pipeline randomly selects reads from the input files (single or paired).
If the inputs are paired, the one-to-one mapping between R1 and R2 is
preserved. FastQ inputs can be gzipped; outputs are gzipped with ``pigz``.
FastA inputs and outputs are uncompressed.


Configuration
~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/downsampling/main/sequana_pipelines/downsampling/config.yaml>`_.
Key sections:

- ``downsampling`` — method (``random`` / ``random_pct``), ``max_entries``,
  ``percent``, ``threads``, and ``input_format`` (``fastq`` / ``fasta``)


Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.10.0    * Migrate to Poetry / pyproject.toml packaging
          * Simplify __init__.py using importlib.metadata
          * Rewrite CLI with rich_click (replaces argparse)
          * Update CI to use setup-micromamba with generate-run-shell
          * Add ``localrules: pipeline``
          * Add ``tools.txt`` and ``environment.yml``
          * Refresh README badges and usage examples
0.9.0     * Maintenance release
0.8.5     * Cope with R1/R2 paired data properly. Improved make file
0.8.4     * Add missing MANIFEST to include missing requirements.txt
0.8.3     * Comply with new API from sequana_pipetools 0.2.4
0.8.2     * Add a --run option to execute the pipeline directly
0.8.1     * Fix input and N in the random selection
0.8.0     **First release.**
========= ====================================================================


Contribute & Code of Conduct
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To contribute to this project, please take a look at the
`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a
`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.
