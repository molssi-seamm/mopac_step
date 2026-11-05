# -*- coding: utf-8 -*-

"""precision="tight" asks the MOPAC MDI engine for a relative tolerance of
0.001 (finite differences of gradients need it; see MOPACStep.TIGHT_TOLERANCE)."""

from mopac_step import MOPACStep


def _argv(monkeypatch, **kwargs):
    monkeypatch.setattr(
        MOPACStep,
        "get_executor_config",
        classmethod(
            lambda cls, executor, options: {
                "installation": "conda",
                "conda": "conda",
                "conda-environment": "seamm-mopac",
                "mdi_script": "mopac_mdi.py",
            }
        ),
    )
    return MOPACStep.get_mdi_engine_command(None, {}, method="PM7", port=1234, **kwargs)


def test_tight_precision(monkeypatch):
    argv = _argv(monkeypatch, precision="tight")
    i = argv.index("--tolerance")
    assert argv[i + 1] == MOPACStep.TIGHT_TOLERANCE == "0.001"


def test_default_precision(monkeypatch):
    assert "--tolerance" not in _argv(monkeypatch)
