# -*- coding: utf-8 -*-

"""MOPAC's batch contract: the batch path gives the MDI path's numbers.

This is the test that protects the decision (Paul, 2026-10-03) that MOPAC's
"energy" is the heat of formation on both paths. It runs real MOPAC (skipped
where MOPAC or pymdi is missing) through ``seamm_exec.Evaluator`` both ways.
"""

import logging
import pathlib
import types

import numpy as np
import pytest

import seamm_exec
from seamm_exec import Evaluator, Geometry

from mopac_step import MOPACStep

pytest.importorskip("mdi")
pytest.importorskip("seamm_mdi")

# Stated tolerances. The heat of formation agrees to 1e-4 kJ/mol (observed
# 2e-7). MOPAC's single-SCF gradient moves by about 0.1% with the SCF
# convergence, which mopactools (the MDI engine) and the MOPAC binary (the batch
# path) stop at different points: on water's O z, 29.116 (binary default),
# 29.082 (SCFCRT=1e-12), 29.072 (engine) and 29.084 kJ/mol/Å (a finite
# difference). So gradients agree to 0.3% + 0.02 kJ/mol/Å.
E_TOL = 1e-4  # kJ/mol
G_RTOL = 3e-3
G_ATOL = 0.02  # kJ/mol/Å

WATERS = [
    [[0.0, 0.0, 0.117], [0.0, 0.757, -0.469], [0.0, -0.757, -0.469]],
    [[0.0, 0.0, 0.120], [0.0, 0.770, -0.470], [0.0, -0.750, -0.460]],
]
ROOT = pathlib.Path("~/SEAMM").expanduser()


def _node(directory):
    return types.SimpleNamespace(
        directory=str(directory),
        global_options={"root": str(ROOT)},
        logger=logging.getLogger("test"),
        variable_exists=lambda name: False,
        flowchart=types.SimpleNamespace(
            executor=seamm_exec.Local(),
            plugin_manager=types.SimpleNamespace(get=lambda name: MOPACStep),
            root_directory=str(directory),
        ),
    )


MC = {
    "level": "MOPAC:SQM@PM6",
    "owner": "MOPAC",
    "type": "SQM",
    "method": "PM6",
    "basis": None,
    "cutoff": None,
    "step": "MOPAC",
    "options": {"mdi_capable": True, "mdi_method_arg": "PM6"},
}


def _evaluate(tmp_path, path):
    with Evaluator(_node(tmp_path / path), MC, path=path) as evaluator:
        for i, xyz in enumerate(WATERS):
            evaluator.submit(Geometry([8, 1, 1], xyz), key=f"w{i}")
        return {r.key: r for r in evaluator.results()}


def test_batch_equals_mdi_heat_of_formation(tmp_path):
    if not (ROOT / "mopac.ini").exists():
        pytest.skip("MOPAC is not configured")
    try:
        mdi = _evaluate(tmp_path, "mdi")
    except Exception as e:
        pytest.skip(f"The MOPAC MDI engine is not available: {e}")
    batch = _evaluate(tmp_path, "batch")
    for key in ("w0", "w1"):
        assert batch[key].ok, batch[key].reason
        # The heat of formation of water at PM6 is about -232 kJ/mol, not a
        # total energy of thousands of kJ/mol
        assert -300 < batch[key].energy < -150
        assert batch[key].energy == pytest.approx(mdi[key].energy, abs=E_TOL)
        assert np.allclose(
            batch[key].gradients, mdi[key].gradients, rtol=G_RTOL, atol=G_ATOL
        )


def test_open_shell_and_periodic_are_refused():
    from mopac_step.batch import get_task

    with pytest.raises(ValueError, match="lowest spin state"):
        get_task(
            Geometry([8, 8], [[0, 0, 0], [1.2, 0, 0]], multiplicity=3), MC, key="o2"
        )
    with pytest.raises(ValueError, match="Periodic"):
        get_task(Geometry([8], [[0, 0, 0]], cell=np.eye(3) * 5), MC, key="box")


def test_parse_aux_heat_and_gradients():
    from mopac_step.batch import parse_aux

    text = (
        " HEAT_OF_FORMATION:KCAL/MOL=-0.554621453D+02\n"
        " GRADIENTS:KCAL/MOL/ANGSTROM[0009]=\n"
        "  0.1D+01-0.2D+01 0.3D+01\n"
        "  4.0 -5.0 6.0  7.0 8.0 -9.0\n"
        " OTHER=1\n"
    )
    heat, gradients = parse_aux(text)
    assert heat == pytest.approx(-55.4621453)
    assert gradients.shape == (3, 3)
    assert gradients[0].tolist() == [1.0, -2.0, 3.0]
