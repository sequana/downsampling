import os
import subprocess
import sys

from click.testing import CliRunner

from sequana_pipelines.downsampling.main import main

from . import test_dir

sharedir = f"{test_dir}/data"


def test_standalone_subprocess(tmp_path):
    wkdir = tmp_path / "test"
    wkdir.mkdir()
    cmd = f"sequana_downsampling --input-directory {sharedir} --working-directory {wkdir} --force"
    subprocess.call(cmd.split())
    assert os.path.exists(wkdir / "config.yaml")


def test_standalone_script(tmp_path):
    wkdir = tmp_path / "test"
    wkdir.mkdir()
    args = [
        "--input-directory", sharedir,
        "--working-directory", str(wkdir),
        "--force",
    ]
    runner = CliRunner()
    runner.invoke(main, args)
    assert os.path.exists(wkdir / "config.yaml")


def test_full(tmp_path):
    wkdir = tmp_path / "wk1"
    wkdir.mkdir()
    cmd = f"sequana_downsampling --input-directory {sharedir} --working-directory {wkdir} --force"
    subprocess.call(cmd.split())
    subprocess.call("bash downsampling.sh".split(), cwd=wkdir)

    wkdir2 = tmp_path / "wk2"
    wkdir2.mkdir()
    cmd = (
        f"sequana_downsampling --input-directory {sharedir} "
        f"--input-pattern *fasta --working-directory {wkdir2} "
        f"--downsampling-method random_pct --downsampling-input-format fasta --force"
    )
    subprocess.call(cmd.split())
    subprocess.call("bash downsampling.sh".split(), cwd=wkdir2)


def test_version():
    cmd = "sequana_downsampling --version"
    subprocess.call(cmd.split())
