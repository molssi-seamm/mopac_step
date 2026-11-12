# -*- coding: utf-8 -*-

"""Settings fingerprints of MOPAC calculations: the task route's record (from
mopac.aux), the MDI engine's (data/mopac_settings.py, completed by seamm_mdi) and
the prediction are one fingerprint, and different settings differ."""

import importlib.resources
import shutil
import subprocess

import numpy as np
import pytest

from seamm_util.fingerprint import calculation_record

from mopac_step import MOPACStep
from mopac_step.batch import aux_version, calculation_record_of, mopac_settings

PM7 = {"level": "MOPAC:SQM@PM7", "method": "PM7", "step": "MOPAC",
       "options": {"mdi_method_arg": "PM7"}}  # fmt: skip
PM6 = {"level": "MOPAC:SQM@PM6", "method": "PM6", "step": "MOPAC",
       "options": {"mdi_method_arg": "PM6"}}  # fmt: skip

AUX = """ START OF MOPAC PROGRAM
 MOPAC_VERSION=23.2.5
 METHOD=PM7
"""


def predict(mc=PM7, version="23.2.5"):
    return MOPACStep.expected_fingerprints(None, mc, kind="energy", version=version)


def test_the_task_routes_record_is_the_prediction():
    assert aux_version(AUX) == "23.2.5"
    record = calculation_record_of(PM7, aux_version(AUX))
    assert record["program"] == "MOPAC"
    assert predict() == [record["fingerprint"]]


def test_the_engines_record_is_the_prediction():
    settings = mopac_settings()
    raw = settings.settings_record("PM7", version="23.2.5")
    assert "fingerprint" not in raw
    done = calculation_record(raw["program"], raw["version"], raw["files"])
    assert predict() == [done["fingerprint"]]


def test_different_settings_differ():
    base = predict()[0]
    assert predict(mc=PM6)[0] != base
    assert predict(version="24.0.0")[0] != base
    settings = mopac_settings()
    for changed in (
        settings.settings_text("PM7", mozyme=True),
        settings.settings_text("PM7", tolerance=0.1),
    ):
        other = calculation_record(
            "MOPAC", "23.2.5", {settings.SETTINGS_FILE: changed}
        )["fingerprint"]
        assert other != base


def test_what_does_not_change_it():
    base = predict()
    assert predict(version="23.2.9") == base  # only major.minor is hashed
    assert (
        MOPACStep.expected_fingerprints(None, PM7, kind="hessian", version="23.2.5")
        == base
    )
    assert predict(version=None) is None  # no version: no prediction
    assert aux_version("no version here") is None


def _engine_available():
    if shutil.which("conda") is None:
        return False
    try:
        from seamm_mdi.mdi_engine import complete_records  # noqa: F401
    except ImportError:
        return False
    result = subprocess.run(
        ["conda", "run", "-n", "seamm-mopac", "python", "-c",
         "import mdi, mopactools.api"],
        capture_output=True,
    )  # fmt: skip
    return result.returncode == 0


def test_real_engine_fingerprint_is_the_prediction():
    if not _engine_available():
        pytest.skip("seamm-mopac MDI engine environment not available")
    from seamm_mdi import MDIEngine

    script = str(importlib.resources.files("mopac_step") / "data" / "mopac_mdi.py")

    def build_argv(hostname, port):
        return [
            "conda", "run", "--live-stream", "-n", "seamm-mopac", "python", script,
            "-mdi",
            f"-role ENGINE -name MOPAC -method TCP -port {port} "
            f"-hostname {hostname}",
            "--method", "PM7", "--charge", "0", "--multiplicity", "1",
        ]  # fmt: skip

    xyz = np.array([[0.0, 0.0, 0.0], [0.7572, 0.5859, 0.0], [-0.7572, 0.5859, 0.0]])
    with MDIEngine(build_argv, elements=[8, 1, 1], timeout=120.0) as engine:
        assert engine.supports("<FINGERPRINT") is True
        engine.set_coordinates(xyz, units="Å")
        engine.energy(units="kcal/mol")
        records = engine.fingerprints()
    record = records["energy"]
    assert record["program"] == "MOPAC" and records["hessian"] is None
    assert [record["fingerprint"]] == predict(version=record["version"])
