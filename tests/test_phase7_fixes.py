# -*- coding: utf-8 -*-
"""A stale success.dat, and the MDI engine's Python (phase 7)."""

from mopac_step.mopac import reuse_previous_run
from mopac_step.mopac_step import _CONDA_PYTHONS, _conda_python


def test_reuse_only_for_the_same_input(tmp_path):
    assert not reuse_previous_run(tmp_path, "PM7\n")  # never ran
    (tmp_path / "mopac.dat").write_text("PM7\nwater\n")
    (tmp_path / "success.dat").write_text("")
    assert reuse_previous_run(tmp_path, "PM7\nwater\n")
    assert not reuse_previous_run(tmp_path, "PM6\nwater\n")  # other input
    assert not (tmp_path / "success.dat").exists()  # the marker is gone


def test_conda_python_from_a_path(tmp_path):
    env = tmp_path / "envs" / "seamm-mopac"
    (env / "bin").mkdir(parents=True)
    (env / "bin" / "python").write_text("")
    _CONDA_PYTHONS.clear()
    assert _conda_python("/no/conda", str(env)) == str(env / "bin" / "python")


def test_conda_python_falls_back_to_python(tmp_path):
    _CONDA_PYTHONS.clear()
    assert _conda_python(str(tmp_path / "no-conda"), "nowhere") == "python"
