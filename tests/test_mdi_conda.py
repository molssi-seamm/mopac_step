# -*- coding: utf-8 -*-

"""The MOPAC MDI engine runs with the conda SEAMM's local executor would use:
CONDA_EXE first (on clusters SEAMM's staging wrapper, which unpacks an
environment kept as an archive onto the node), else the ini's conda. xtb-step's
twin of this launch failed on ARC with an archive-only environment (SEAMM job
6088, 2026-11-26)."""

import mopac_step
from mopac_step import MOPACStep

CONFIG = {
    "installation": "conda",
    "conda": "/apps/miniforge/bin/conda",
    "conda-environment": "seamm-mopac",
    "mdi_script": "mopac_mdi.py",
}


def _argv(monkeypatch, config):
    asked = []
    monkeypatch.setattr(
        MOPACStep,
        "get_executor_config",
        classmethod(lambda cls, executor, options: dict(config)),
    )

    def python_of(conda, environment):
        asked.append(conda)
        return f"/envs/{environment}/bin/python"

    monkeypatch.setattr(mopac_step.mopac_step, "_conda_python", python_of)
    argv = MOPACStep.get_mdi_engine_command(None, {}, method="PM7", port=1234)
    return argv, asked


def test_conda_exe_wins(monkeypatch):
    monkeypatch.setenv("CONDA_EXE", "/projects/seamm/SEAMM/bin/seamm-conda")
    argv, asked = _argv(monkeypatch, CONFIG)
    assert argv[:5] == [
        "/projects/seamm/SEAMM/bin/seamm-conda",
        "run",
        "--live-stream",
        "-n",
        "seamm-mopac",
    ]
    # the interpreter is looked up with the same conda
    assert asked == ["/projects/seamm/SEAMM/bin/seamm-conda"]


def test_the_ini_conda_without_conda_exe(monkeypatch):
    monkeypatch.delenv("CONDA_EXE", raising=False)
    argv, asked = _argv(monkeypatch, CONFIG)
    assert argv[0] == asked[0] == "/apps/miniforge/bin/conda"
    config = {k: v for k, v in CONFIG.items() if k != "conda"}
    assert _argv(monkeypatch, config)[0][0] == "conda"
