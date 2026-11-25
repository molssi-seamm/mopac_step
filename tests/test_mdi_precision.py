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


def test_the_engine_declares_one_thread():
    """The driver reports the engine's cores from mdi_engine_threads; it must
    match the engine script, which pins OpenMP and MKL to one thread."""
    import importlib.resources

    assert MOPACStep.mdi_engine_threads == 1
    script = importlib.resources.files("mopac_step") / "data" / "mopac_mdi.py"
    text = script.read_text()
    assert 'os.environ.setdefault("OMP_NUM_THREADS", "1")' in text
    assert 'os.environ.setdefault("MKL_NUM_THREADS", "1")' in text
