This is is the **downsampling** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project

:Overview: downsample NGS data sets
:Input: a set of FastQ or FASTA files 
:Output: a set of downsampled files
:Status: mature
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_downsampling


Usage
~~~~~

::

    sequana_pipelines_downsampling --help
    sequana_pipelines_downsampling --input-directory DATAPATHH
    sequana_downsampling --downsampling-method random --downsampling-max-entries 100


This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd downsampling
    sh downsampling.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s downsampling.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- sequana
- pigz

.. .. image:: https://raw.githubusercontent.com/sequana/sequana_downsampling/master/sequana_pipelines/downsampling/dag.png


Details
~~~~~~~~~

This pipeline runs **downsampling** in parallel on the input fastq or fasta files (paired or not).

It can take as input a set of FastQ files, or FastA files. by
default, the pipeline with randomly select 1000 entries from each input files.
You can increase this number using --downsampling-max-entries option. If you
prefer to select a percentage of the entries instead, you can change the
downsamping method as follows::

    --downsampling-method random_pct

and change the value if needed (default is 10%)::

    --downsampling-percent 20

Note that input FastQ and FastA files can be gzipped. Output files are gzipped.



Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_downsampling/master/sequana_pipelines/downsampling/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 


Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.8.4     * add missing MANIFEST to include missing requirements.txt
0.8.3     * comply with new API from sequana_pipetools 0.2.4
0.8.2     * add a --run option to execute the pipeline directly
0.8.1     * fix input and N in the random selection
0.8.0     **First release.**
========= ====================================================================


